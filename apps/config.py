import os


class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MONGOALCHEMY_DATABASE = 'mongod'
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "ivana.zaccheddu88@gmail.com"
    MAIL_PASSWORD = "E12009go"