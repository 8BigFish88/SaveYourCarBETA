import os
from os import environ


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY2')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI2')
    FLASK_ADMIN_SWATCH = os.environ.get('FLASK_ADMIN_SWATCH')
    MONGO_URI = 'mongodb+srv://quadrophenia:password4321@cluster0-unq9q.mongodb.net/test?retryWrites=true&w=majority'
    MONGO_ENGINE = 'the-config.cfg'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')