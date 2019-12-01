from apps import db, login_manager, admin
from flask_login import UserMixin
import flask_admin as admin
from flask_admin.contrib.sqla import ModelView
from apps.appUser.models import User
from apps.appCar.models import Car, CarDataValue, CarData
from flask_admin import helpers, expose




admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Car, db.session))
admin.add_view(ModelView(CarDataValue, db.session))
admin.add_view(ModelView(CarData, db.session))