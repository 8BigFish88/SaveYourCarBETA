from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from app import mongo

reminders = Blueprint('reminders', __name__)

@reminders.route("/notifiche")
def notifiche():
    reminder_collection = mongo.db.reminder
    reminder_collection.insert({ 'title' : 'ReminderAssicurazione', 'text' : 'Devi Fare l Assicurazione!' })
    return 'Inserito Reminder'

@reminders.route('/find')
def find():
    reminder_collection = mongo.db.reminder
    reminderT = reminder_collection.find_one({ 'title' : 'ReminderRevisione' })
    return f'<h1>ReminderT:{ reminderT["title"] } Text:{reminderT["text"]}</h1>'
    #return render_template('index.html')

