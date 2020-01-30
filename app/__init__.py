from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mongoalchemy import MongoAlchemy
from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.config import Config
from flask_admin import helpers, expose
from app.logger import logger
from app.settings.loggings.messages import Log
from flask_cors import CORS, cross_origin

log = Log()

db = SQLAlchemy()
migrate = Migrate()
#client = pymongo.MongoClient("mongodb+srv://quadrophenia:password4321@cluster0-unq9q.mongodb.net/test?retryWrites=true&w=majority")
mongo = PyMongo()
#db2 = client.test

api = Api()
cors = CORS()


#db2 = MongoAlchemy()
#db2 = MongoEngine()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    logger.info('%s' %log.start )
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    mongo.init_app(app)
    bcrypt.init_app(app)
    api.init_app(app, version='1.0', title='SYC API')
    login_manager.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    from app.users.controllers import users
    from app.cars.controllers import cars
    from app.reminders.controllers import reminders
    from app.main.controllers import main
    from app.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(cars)
    app.register_blueprint(reminders)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    from app.users.models import User
    from app.cars.models import Car, CarDataValue, CarData
    from app.API.api import POST_Register_User
    from app.API.api import GET_Users

    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Car, db.session))
    admin.add_view(ModelView(CarDataValue, db.session))
    admin.add_view(ModelView(CarData, db.session))

    api.add_resource(POST_Register_User,'/api/v1.0/user')
    api.add_resource(GET_Users,'/api/v1.0/users')

    return app
