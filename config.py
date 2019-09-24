import os


class Config:
    # General Config
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_APP = os.environ.get('FLASK_APP')

class DevConfig(Config):
    # General
    FLASK_DEBUG=1

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = 0

class TestConfig(Config):
    # General
    FLASK_DEBUG=1
    TESTING=True

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = 0

    # Forms
    WTF_CSRF_ENABLED=False
