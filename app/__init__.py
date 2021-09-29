from flask import Flask, config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
#######################
#### Configuration ####
#######################

# Create the instances of the Flask extensions in the global scope,
# but without any arguments passed in. These instances are not
# attached to the Flask application at this point.

database = SQLAlchemy()
mail = Mail()

######################################
#### Application Factory Function ####
######################################

def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config_from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    return app

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)

    database.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    # Import the blueprints
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    pass





