import os,tempfile

class Config(object):

    # Application configuration 1
    SECRET_KEY = "02f104f1-9484-4699-a48b-abc900c53ceb"
    APP_HOST = "https://www.saferoomapp.com:5000"		
	
    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CACHE_DIR = os.path.join(BASE_DIR,"cache")
    TMP_DIR = os.path.join(BASE_DIR,"static")
    UPLOADS_DIR = os.path.join(BASE_DIR,"static")	
	

class ProductionConfig(Config):
	pass

class TestConfig(Config):
    db_file = tempfile.NamedTemporaryFile()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:admin@127.0.0.1:3306/ca"
    SQLALCHEMY_TRACK_MODIFICATIONS = True