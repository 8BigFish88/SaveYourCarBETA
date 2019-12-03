from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mongoalchemy import MongoAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from apps.config import Config
from flask_admin import helpers, expose
import logging

db = SQLAlchemy()
migrate = Migrate()
db2 = MongoAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
admin = Admin(name='microblog', template_mode='bootstrap3')
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    logging.basicConfig(filename='syc.log', level=logging.INFO)
    logging.info('Started')
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    db2.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    mail.init_app(app)

    from apps.appUser.controllers import users
    from apps.appCar.controllers import cars
    #from apps.appReminder.controllers import reminders
    from apps.main.controllers import main
    from apps.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(cars)
    #app.register_blueprint(reminders)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    logging.info('Finished')


    return app
