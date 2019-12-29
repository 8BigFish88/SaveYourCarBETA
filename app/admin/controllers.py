from app import db, login_manager, admin
from flask_login import UserMixin
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView
from app.users.models import User
from app.cars.models import Car, CarDataValue, CarData
from flask_admin import helpers, expose




admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Car, db.session))
