import os
import secrets
from PIL import Image
from app.cars.models import Car, CarDataValue, CarData
from app import db
from datetime import datetime  
from datetime import timedelta  
from flask import flash, url_for, current_app
from app import mongo
from app.settings.messages import Flash,Error
flashM=Flash()
errorM=Error()


def InsertCarDataValue(carValues,form):
	for i in carValues:
          if i.id_CarData==1:
             i.valueInt = form.kmattuali.data
          elif i.id_CarData==2:
             i.valueDate = form.dataRevisione.data
          elif i.id_CarData==3:
             i.valueInt = form.kmTagliando.data
          elif i.id_CarData==4:
              i.valueDate = form.dataAssicurazione.data
          elif i.id_CarData==5:
             i.valueDate = form.dataBollo.data
          elif i.id_CarData==6:
             i.valueInt  = form.kmMedi.data

def AddCarValueToDb(car,form):
	carValue1 = CarDataValue(valueInt = form.kmattuali.data,
                                           id_CarData = 1, car_author = car )
	db.session.add(carValue1)
	carValue2 = CarDataValue(valueDate = form.dataRevisione.data,
                                           id_CarData = 2, car_author = car )
	db.session.add(carValue2)
	carValue3 = CarDataValue(valueInt = form.kmTagliando.data,
                                           id_CarData = 3, car_author = car )
	db.session.add(carValue3)
	carValue4 = CarDataValue(valueDate = form.dataAssicurazione.data,
                                           id_CarData = 4, car_author = car )
	db.session.add(carValue4)
	carValue5 = CarDataValue(valueDate = form.dataBollo.data,
                                           id_CarData = 5, car_author = car )
	db.session.add(carValue5)
	carValue6 = CarDataValue(valueInt = form.kmMedi.data,
                                           id_CarData = 6, car_author = car )
	db.session.add(carValue6)

def GetKm(car, carvalues):
	for carvalue in carvalues:
		if carvalue.id_CarData == 6:
			kmMedi = carvalue.valueInt
			return kmMedi

def GetDateDetection(car, carvalues):
	for carvalue in carvalues:
		if carvalue.id_CarData == 1:
			rilievo = [carvalue.valueDate, carvalue.valueInt]
			return rilievo

def assicurazione(car, value):
	 if (datetime.now() >= value.valueDate - timedelta(days=30)) and (value.id_CarData == 4):
		 return True
	 else:
		 return False
		
def bollo(car, value):
	 if (datetime.now() >= value.valueDate - timedelta(days=30)) and (value.id_CarData == 5):
		 return True
	 else:
		 return False

def revisione(car, value):
	 if ((((datetime.now() - value.valueDate >= timedelta(days=730) - timedelta(days=30)) 
				and 
				(datetime.now() - car.matriculation >= timedelta(days=1460)) 
				)
				or 
				(
				(datetime.now() - car.matriculation < timedelta(days=1460))
				and 
				(timedelta(days=1460) - (datetime.now() - car.matriculation) <= timedelta(days=30)) 
				)
				)
				and 
				(value.id_CarData == 2)):  
		 return True
	 else:
		 return False

def tagliando(car, value, kmMedi, rilievo):
	 if ((value.id_CarData == 3) 
			and
			((rilievo[1] + (kmMedi*((datetime.now() - rilievo[0])/timedelta(days=7))))-value.valueInt > 30000)
			):
		 return True
	 else:
		 return False

def FlashReminders(car,carvalues):
	kmMedi = GetKm(car, carvalues)
	rilievo = GetDateDetection(car, carvalues)
	reminder_collection = mongo.db.reminder
	reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
	for value in carvalues:
		if	assicurazione(car, value):
			flash( reminder["reminders"]["ASSICURAZIONE"] , 'danger')
		if  bollo(car,value):
			flash( reminder["reminders"]["BOLLO"] , 'danger')   
		if  revisione(car,value):
			flash( reminder["reminders"]["REVISIONE"] , 'danger')  
		if  tagliando(car, value, kmMedi, rilievo):
			flash( reminder["reminders"]["TAGLIANDO"] , 'danger') 

def listCarReminders(car,carvalues):
	kmMedi = GetKm(car, carvalues)
	rilievo = GetDateDetection(car, carvalues)
	reminder_collection = mongo.db.reminder
	reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
	reminders_list = []
	for value in carvalues:
		if	assicurazione(car, value):
			reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
			reminder["reminders"]['ASSICURAZIONE']="%s"%flashM.carsAssicurazione
			reminder_collection.save(reminder)
			reminders_list.append(reminder["reminders"]["ASSICURAZIONE"])
		if  bollo(car,value):
			reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
			reminder["reminders"]['BOLLO']="%s"%flashM.carsBollo
			reminder_collection.save(reminder)
			reminders_list.append(reminder["reminders"]["BOLLO"])  
		if  revisione(car,value):
			reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
			reminder["reminders"]['REVISIONE']="%s"%flashM.carsRevisione
			reminder_collection.save(reminder)
			reminders_list.append(reminder["reminders"]["REVISIONE"])  
		if  tagliando(car, value, kmMedi, rilievo):
			reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
			reminder["reminders"]['TAGLIANDO']="%s"%flashM.carsTagliando
			reminder_collection.save(reminder)
			reminders_list.append(reminder["reminders"]["TAGLIANDO"])  
	return reminders_list


def save_car_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/car_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
   
    return picture_fn

		
		
	

