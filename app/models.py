from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import datetime,json,hashlib,base64,uuid
from M2Crypto import BIO,X509
from passlib.apps import custom_app_context as pwd_context
from OpenSSL import crypto, SSL
from app.libs.functions import md5_string
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
db = SQLAlchemy()


# Initializing models
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255),default='',nullable=False,index=True)
    email = db.Column(db.String(255),default='',nullable=False)
    password = db.Column(db.String(255),nullable=True,default="")
    subject = db.Column(db.String(256),nullable=False,index=True)
    certificate = db.relationship("Certificate", uselist=False, back_populates="user")

    def __init__(self):
    	pass

    def __repr__(self):
    	return "<User, name=%r, email=%r,subject=%r>" % (self.name,self.email,self.subject)

    def as_dict(self):
    	user =  {c.name: getattr(self, c.name) for c in self.__table__.columns}
    	user.pop('password')
        return user

    def update(self,data):
        if "name" in data:
            if data['name'] != "":
                self.name = data['name']
        if "email" in data:
            if data['email'] != "":
                self.email = data['email']
        if "subject" in data:
            if data['subject'] != "":
                self.subject = data['subject']

    @staticmethod
    def from_json(json):
        user = User()
        user.name = json['name']
        user.email = json['email']
        user.subject = json['subject']
        user.hash_password(json['password'])
        return user
    
    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

#### Certificate Authority Model
class CertificateAuthority(db.Model):
    __tablename__ = "ca"
    id = db.Column(db.Integer,primary_key=True)
    root_ca = db.Column(db.Integer,default=0)
    name = db.Column(db.String(256),index=True)
    dscr = db.Column(db.String(256),index=True)
    subject_dn = db.Column(db.String(128),index=True)
    extensions = db.Column(db.Text,index=False)
    created = db.Column(db.DateTime,default=datetime.datetime.now()) 

    def __init__(self,name=None,subject_dn=""):
        self.name = name
        self.subject_dn = subject_dn

    def __repr__(self):
        return "<Certificate Authority: %r, Subject DN=%r" % (self.name,self.subject_dn)

    # Relationships
    keys = db.relationship('Key',cascade="all,delete")
    certificates = db.relationship("Certificate",cascade="all,delete")
    crls = db.relationship("CRL",cascade="all,delete")


#### Model used to describe the CA keys (public and private keypairs)
class Key(db.Model):
    __tablename__ = "ca_keys"
    # Columns
    id = db.Column(db.Integer,primary_key=True)
    ca = db.Column(db.Integer,db.ForeignKey('ca.id'))
    private = db.Column(db.Text)
    public = db.Column(db.Text)
    expires_in = db.Column(db.DateTime)

    def __init__(self):
        pass
    def __repr__(self):
        return "Key, private=%r, public=%r" % (self.private,self.public)
        
    
    def generate_private_key(self,password,length):
        self.pKey = crypto.PKey()
        self.pKey.generate_key(crypto.TYPE_RSA, int(length))
        # Assigning private key
        self.private = crypto.dump_privatekey(crypto.FILETYPE_PEM,self.pKey,cipher="AES256",passphrase=str(password))
    
    def generate_public_key(self,json,root_key=None,root_ca=None,ca_id=None):
    
        # Generating the serial number
        md5_hash = hashlib.md5()
        md5_hash.update(str(uuid.uuid4()))
        serial = int(md5_hash.hexdigest(), 24)
        
        # Generating the certificate
        ca_cert = crypto.X509()
        if "C" in json['subjectDN']:
            ca_cert.get_subject().C = json['subjectDN']['C']
        if "O" in json['subjectDN']:
            ca_cert.get_subject().O = json['subjectDN']['O']
        if "OU" in json['subjectDN']:
            ca_cert.get_subject().OU = json['subjectDN']['OU']
        if "CN" in json['subjectDN']:
            ca_cert.get_subject().CN = json['subjectDN']['CN']
        ca_cert.set_version(2)
        ca_cert.set_serial_number(serial)
        
        ca_cert.gmtime_adj_notBefore(0)
        ca_cert.gmtime_adj_notAfter(int((self.expires_in - datetime.datetime.now()).total_seconds()))
        ca_cert.set_pubkey(self.pKey)
        ca_cert.set_issuer(ca_cert.get_subject())
        ca_cert.add_extensions([crypto.X509Extension("basicConstraints", True,"CA:TRUE"),crypto.X509Extension("keyUsage", True,"keyCertSign, cRLSign"),crypto.X509Extension("subjectKeyIdentifier", False, "hash",subject=ca_cert),crypto.X509Extension("authorityKeyIdentifier", False,'keyid,issuer', issuer=ca_cert)])
        
        # Signing the key
        ca_cert.sign(self.pKey, str(json['hash']))
        
        # Setting the public key
        self.public = crypto.dump_certificate(crypto.FILETYPE_PEM,ca_cert)


#### Model used to describe the Certificate
class Certificate(db.Model):
    __tablename__ = "certificates"

    # Columns
    id = db.Column(db.Integer,primary_key=True)
    ca = db.Column(db.Integer,db.ForeignKey('ca.id'))                     # The certificate authority that issued this certificate
    uid = db.Column(db.Integer,db.ForeignKey('users.id')) 
    name = db.Column(db.String(128),index=True,nullable=False)
    serial = db.Column(db.String(64))                                  # Certificate serial number
    public = db.Column(db.Text)                                        # Public key
    p12 = db.Column(db.Text)                                           # PFX data in Base
    status = db.Column(db.Integer,default=1)                           # Current status: 1 = Active, 2 = Revoked, 3 = Expired
    created = db.Column(db.DateTime,default=datetime.datetime.now())
    code_revoke = db.Column(db.Integer,default=-1)                     # Revocation code
    reason_revoke = db.Column(db.String(256),nullable=True,default="") # Revocation reason (if any)
    date_revoke = db.Column(db.DateTime,nullable=True,default=None)    # Revocation date
    
    # Relationship
    user = db.relationship("User", uselist=False, back_populates="certificate")
    
    # Initializing the certificate
    def __init__(self):
        pass

    def __repr__(self):
        return "<Certificate, serial=%r, status=%r, pfxdata=%r" % (self.serial,self.status,self.p12)

    # Relationship
    authority = db.relationship('CertificateAuthority')
       

    @staticmethod
    def create_stack(recipients):
        
        # Getting the IDs of recipients
        ids = [item for item in recipients]
        
        # Getting a list of certificates (public keys)
        public_keys = Certificate.query.with_entities(Certificate.public,Certificate.serial).filter(Certificate.id.in_(ids)).all()
                
        # Creating the array of serial numbers
        recipients = [item[1] for item in public_keys]
                
        # Checking that keys are not empty
        if len(public_keys) == 0:
            return (None,400,"Keys not found",[])

        # Creating the BIOs
        bios = []
        for key in public_keys:
            bios.append(BIO.MemoryBuffer(key.public.encode("utf-8")))

        # Checking that we have at least one recipient
        if len(bios) == 0:
            return (None,404,"Recipients not found",[])

        # Creating the stack
        stack = X509.X509_Stack()
        for bio in bios:
            stack.push(X509.load_cert_bio(bio))
        return (stack,200,"",recipients)
	
    def as_dict(self):
        certificate =  {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return certificate
        

class Template(db.Model):
    __tablename__ = "templates"

    # Columns
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),index=True)
    dscr = db.Column(db.String(256),index=True)
    extensions = db.Column(db.Text)

    def __init__(self,name,dscr):
        self.name = name
        self.dscr = dscr

    def set_extensions(self,extensions=[]):
        self.extensions = json.dumps(extensions)

    def __repr__(self):
        return "<Template, name=%r, dscr=%r, extensions=%r" % (self.name,self.dscr,self.extensions)

class CRL(db.Model):
    __tablename__ = "crls"

    # Columns
    id = db.Column(db.Integer,primary_key=True)
    ca = db.Column(db.Integer,db.ForeignKey('ca.id'))
    created = db.Column(db.DateTime,nullable=True,default=datetime.datetime.utcnow)
    crl = db.Column(db.LargeBinary,nullable=False)

class Administrator(db.Model):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256),index=True)
    email = db.Column(db.String(64),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    
    def __init__(self,name=None,email=None):
    	self.name = name
    	self.email = email
        
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)
        
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

   	def __repr__(self):
   		return '<Administrator name=%r, email=%r' % (self.name,self.email)
        
    def as_dict(self):
    	admin =  {c.name: getattr(self, c.name) for c in self.__table__.columns}
    	admin.pop('password_hash')
        return admin
        
    def generate_auth_token(self, expiration = 86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })
        
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return False # valid token, but expired
        except BadSignature:
            return False # invalid token
        admin = Administrator.query.get(data['id'])
        return admin