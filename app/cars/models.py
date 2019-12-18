from datetime import datetime
from app import db, login_manager, admin
from flask_admin.contrib.sqla import ModelView

class CarData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carDataName = db.Column(db.String(100), nullable=False)
    dataType = db.Column(db.Boolean(), nullable=False)
    carDataValues = db.relationship('CarDataValue', backref='category', lazy=True)

    def __repr__(self):
        return f"CarData('{self.carData}', '{self.dataType}')"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    fuel = db.Column(db.String(100), nullable=False)
    matriculation = db.Column(db.DateTime, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    carDataValues = db.relationship('CarDataValue', backref='car_author', lazy=True)
    
    def __repr__(self):
        return f"Car('{self.name}', '{self.matriculation}', '{self.fuel}','{self.image_file}', {self.carDataValues}')"

class CarDataValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valueInt = db.Column(db.Integer, nullable=True, default=0)
    valueDate = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    id_CarData = db.Column(db.Integer, db.ForeignKey('car_data.id'), nullable=False)
    id_Car = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    #relationReminderCarData = db.relationship('RelationReminderCarData', backref='owner', lazy=True)

    def __repr__(self):
        return f"Car('{self.valueInt}', '{self.valueDate}')"


