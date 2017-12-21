# Import section
import datetime,json,atexit,requests
from flask import Flask,jsonify,request,render_template,send_from_directory
from config import DevelopmentConfig
from flask_cors import CORS, cross_origin
from apscheduler.scheduler import Scheduler
from models import db

def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)    
    cors = CORS(app,resources={r"/*":{"origins":"*"}},allow_headers=['Authorization','Content-Type'])
    db.init_app(app)
    
    cron = Scheduler(daemon=True)
    cron.start()

    @app.route('/')
    def index():
        return render_template("index.html")    

    # Importing Blueprints
    from controllers.cas import blueprint_cas
       
    # Registering blueprints
    app.register_blueprint(blueprint_cas)
    

    # Custom HTTP error handlers
    @app.errorhandler(400)
    def custom_400(error):
        print error
        return jsonify(message=error.description['message']),400

    @app.errorhandler(401)
    def custom_401(error):
        return jsonify(message=error.description['message']),401

    @app.errorhandler(403)
    def custom_403(error):
        return jsonify(message=error.description['message']),403

    @app.errorhandler(404)
    def custom_404(error):
        return jsonify(message="Item or resource not found"),404

    @app.errorhandler(405)
    def custom_405(error):
        return jsonify(message="Not allowed"),405

    @app.errorhandler(500)
    def custom_500(error):
        return jsonify(message=error.description['message']),500

    #@app.errorhandler(Exception)
    #def unhandled_exception(e):
    #    return jsonify(message=str(e)),500
    
    # Shutdown your cron thread if the web process is stopped
    atexit.register(lambda: cron.shutdown(wait=False))

    return app
