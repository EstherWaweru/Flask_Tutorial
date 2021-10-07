from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from celery import Celery
from config import Config

#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions in the global scope,
# but without any arguments passed in. These instances are not
# attached to the Flask application at this point.

database = SQLAlchemy()
from .models import User
mail = Mail()
#celery initialization
celery = Celery(__name__,backend = Config.CELERY_RESULT_BACKEND, broker = Config.CELERY_BROKER_URL )


######################################
#### Application Factory Function ####
######################################

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)
    # Configure celery
    celery.conf.update(app.config)
    
    initialize_extensions(app)
    
    register_blueprints(app)
    
    with app.app_context():
        database.create_all()

    return app

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)

    database.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    # Import the blueprints
    from .users import users_bp
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    app.register_blueprint(users_bp)










