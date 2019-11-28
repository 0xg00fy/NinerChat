import os


class Config:
    # General Config
    SECRET_KEY = 'butterlettuce'
    FLASK_APP = os.environ.get('FLASK_APP')

class DevConfig(Config):
    # General

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = 0

class TestConfig(Config):
    # General
    TESTING=True
    SECRET_KEY = 'test'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = 0

    # Forms
    WTF_CSRF_ENABLED=False
