from apps import db2


class Reminder(db2.Document):
	category = db2.StringField()
	text = db2.StringField()



"""
from datetime import datetime
from apps import db, login_manager

class ReminderText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reminderText = db.Column(db.String(255), nullable=False)
    relationReminderCarData = db.relationship('CarDataReminder', backref='category', lazy=True)

    def __repr__(self):
        return f"ReminderText('{self.reminderText}')"

class RelationReminderCarData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_CarDataValue = db.Column(db.Integer, db.ForeignKey('car_data_value.id'), nullable=False)
    id_ReminderText = db.Column(db.Integer, db.ForeignKey('reminder_text.id'), nullable=False)
"""
