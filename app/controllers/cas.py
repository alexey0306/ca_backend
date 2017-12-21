# Import section
import json,datetime,time
from flask import Blueprint, abort,request,render_template,jsonify, Response
from sqlalchemy import desc
from app.models import db,CertificateAuthority, Key
from dateutil.relativedelta import relativedelta

# Initializing the blueprint
blueprint_cas = Blueprint("ca",__name__,url_prefix="/ca")

@blueprint_cas.route("/list",methods=["GET"])
def list_ca():

    # Getting filter
    result = CertificateAuthority.query.with_entities(CertificateAuthority.id,CertificateAuthority.name,CertificateAuthority.dscr).all()    

    # Prepare and send response
    cas = []
    for ca in result:
        cas.append({"id":ca.id,"name":ca.name,"description":ca.dscr})

    return jsonify(cas)
    
@blueprint_cas.route("/create",methods=["POST"])
def create_ca():
    
    # Importing additional functions
    from OpenSSL import crypto, SSL
    
    # Processing JSON data
    data = request.get_json()
    
    # Creating new CA
    ca = CertificateAuthority(name=data['name'],subject_dn=json.dumps(data['subjectDN']))
    ca.dscr = data['dscr']
    ca.extensions = json.dumps(data['extensions'])
    
    # Adding the CA to the database
    db.session.add(ca)
    db.session.commit()
    
    # Creating a pair of keys
    root_key = None
    root_cert = None
    key = Key()
    key.expires_in = datetime.datetime.now() + relativedelta(months=data['valid'])
    key.generate_private_key(data['pass'],data['keylen'])
    key.generate_public_key(data,root_key,root_cert,ca.id)
    
    # Adding to database
    ca.keys.append(key)
    db.session.add(key)
    db.session.commit()
    
    return jsonify([]),201