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

cars = Blueprint('cars', __name__, template_folder='templates')
                     

@cars.route("/auto")
@login_required
def auto():
    cars = Car.query.all()
    return render_template('auto.html', title=current_user.username, cars=current_user.cars)

@cars.route("/car/new_car", methods=['GET', 'POST'])
@login_required
def new_car():
    form = CarForm()
    if form.validate_on_submit():
       car = Car(name=form.name.data, fuel= form.fuel.data, matriculation=form.matriculation.data, author=current_user)
       db.session.add(car)
       db.session.commit()
       carDataValue1 = CarDataValue(valueInt = form.kmattuali.data, id_CarData = 1, car_author = car )
       carDataValue2 = CarDataValue(valueDate = form.dataRevisione.data, id_CarData = 2, car_author = car )
       db.session.add(carDataValue1)
       db.session.add(carDataValue2)
       db.session.commit()
       flash('I dati della tua auto sono stati salvati !', 'success')
       return redirect(url_for('main.home'))
       image_file = url_for('cars.car_pics', filename=car.image_file)
    return render_template('new_car.html', title='New Car',
                            form=form, legend='Nuova Auto')

@cars.route("/car/<int:car_id>")
def car(car_id):
    car = Car.query.get(car_id)
    print(car)
    return render_template('car.html', title=car.name, car=car)

@cars.route("/car/<int:car_id>/update", methods=['GET', 'POST'])
@login_required
def update_car(car_id):
    car = Car.query.get(car_id)
    carDataValue = CarDataValue.query.filter(CarDataValue.car_author.any(id_Car=CarDataValue.car_author.id)).all()
    form = CarForm()
    if form.validate_on_submit():
        car.name = form.name.data
        car.fuel = form.fuel.data
        car.matriculation = form.matriculation.data
        carDataValue.carValueInt = form.kmattuali.data
        carDataValue.carValuedDate = form.dataRevisione.data
        db.session.commit()
        flash('I dati della tua auto sono stati aggiornati!', 'success')
        return redirect(url_for('cars.car.html', car_id=car.id))
    elif request.method == 'GET':
        form.name.data = car.name
        form.fuel.data = car.fuel
        form.matriculation.data = car.matriculation
        form.kmattuali.data = car_data_value.valueInt
        form.dataRevisione.data = car_data_value.valueDate
    image_file = url_for('car_pics', filename=car.image_file)
    return render_template('new_car.html', title='Update Car',
                           image_file=image_file, form=form, legend='Update Car')

@cars.route("/car/<int:car_id>/delete", methods=['POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('La tua auto è stata rimossa!', 'success')
    return redirect(url_for('main.home'))