import os
##Configuration files
# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    # openssl rand -hex 32
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # Flask-Mail Configuration - GMail
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', default = False)
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', default = True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', default='')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', default='')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', default='')
    #celery configurations
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')


class ProductionConfig(Config):
    FLASK_ENV = 'production'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', default = f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}")

