import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from apps import db, bcrypt
from apps.appCar.forms import CarForm
from apps.appUser.models import User
from apps.appCar.models import Car, CarDataValue, CarData
from flask_login import login_user, current_user, logout_user, login_required
from jinja2 import TemplateNotFound
from datetime import datetime
from apps.appCar.utils import *
from apps import mongo
import logging

cars = Blueprint('cars', __name__, template_folder='templates')
                     

@cars.route("/auto")
@login_required
def auto():  
    for car in current_user.cars:
      FlashReminders(car, car.carDataValues)  
    return render_template('auto.html', title=current_user.username, cars=current_user.cars)

@cars.route("/car/new_car", methods=['GET', 'POST'])
@login_required
def new_car():
    form = CarForm()
    if form.validate_on_submit():
       car = Car(name=form.name.data, fuel= form.fuel.data, matriculation=form.matriculation.data, author=current_user)
       db.session.add(car)
       AddCarValueToDb(car,form)
       db.session.commit()
       reminder_collection = mongo.db.reminder
       reminder_collection.insert({ 'title' : car.name.upper() , 'reminders' : {} })
       flash('I dati della tua auto sono stati salvati !', 'success')
       return redirect(url_for('main.home'))
       image_file = url_for('static', filename='car_pics/' + car.image_file)
    else:
       logging.info('campo mancante o errato')
    return render_template('new_car.html', title='New Car',
                            form=form, legend='Nuova Auto')

@cars.route("/car/<int:car_id>")
def car(car_id):
    car = Car.query.get(car_id)
    carValues = CarDataValue.query.filter_by(id_Car = car.id).all()
    FlashReminders(car, carValues)
    return render_template('car.html', title=car.name, car=car)

@cars.route("/car/<int:car_id>/update", methods=['GET', 'POST'])
@login_required
def update_car(car_id):
    car = Car.query.get(car_id)
    carValues = CarDataValue.query.filter_by(id_Car = car.id).all()
    carData = CarData.query.all()
    form = CarForm()
    if form.validate_on_submit():
        car.name = form.name.data
        car.fuel = form.fuel.data
        car.matriculation = form.matriculation.data
        InsertCarDataValue(carValues,form)
        db.session.commit()
        flash('I dati della tua auto sono stati aggiornati!', 'success')
        return redirect(url_for('cars.car', car_id=car.id))
    elif request.method == 'GET':
        form.name.data = car.name
        form.fuel.data = car.fuel
        form.matriculation.data = car.matriculation
        for i in carValues:
          if i.id_CarData==1:
             form.kmattuali.data = i.valueInt
          elif i.id_CarData==2:
             form.dataRevisione.data = i.valueDate
          elif i.id_CarData==3:
             form.kmTagliando.data = i.valueInt
          elif i.id_CarData==4:
             form.dataAssicurazione.data = i.valueDate
          elif i.id_CarData==5:
             form.dataBollo.data = i.valueDate
          elif i.id_CarData==6:
             form.kmMedi.data = i.valueInt
    image_file = url_for('static', filename='car_pics/' + car.image_file)
    return render_template('new_car.html', title='Update Car',
                           image_file=image_file, form=form, legend='Update Car')

@cars.route("/car/<int:car_id>/delete", methods=['POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get(car_id)
    carValues = CarDataValue.query.filter_by(id_Car = car.id).all()
    db.session.delete(car)
    for i in carValues:
      db.session.delete(i)
    db.session.commit()
    flash('La tua auto è stata rimossa!', 'success')
    return redirect(url_for('main.home'))