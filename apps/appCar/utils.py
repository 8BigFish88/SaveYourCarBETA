from apps.appCar.models import Car, CarDataValue, CarData
from apps import db
from datetime import datetime  
from datetime import timedelta  
from flask import flash
from apps import mongo

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
	for value in carvalues:
		if	assicurazione(car, value):
			reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
			reminder["reminders"]['ASSICURAZIONE']=": Devi fare l'ASSICURAZIONE!Affrettati!"
			reminder_collection.save(reminder)
			flash( reminder["title"] + reminder["reminders"]["ASSICURAZIONE"] , 'danger')
		if  bollo(car,value):
			reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
			reminder["reminders"]['BOLLO']=": Devi rinnovare il BOLLO!Affrettati!"
			reminder_collection.save(reminder)
			flash( reminder["title"] + reminder["reminders"]["BOLLO"] , 'danger')   
		if  revisione(car,value):
			reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
			reminder["reminders"]['REVISIONE']=": Quest'auto ha bisogno di una REVISIONE!Affrettati!"
			reminder_collection.save(reminder)
			flash( reminder["title"] + reminder["reminders"]["REVISIONE"] , 'danger')  
		if  tagliando(car, value, kmMedi, rilievo):
			reminder = reminder_collection.find_one({ 'title' : car.name.upper() })
			reminder["reminders"]['TAGLIANDO']=": Quest'auto ha bisogno di un TAGLIANDO!"
			reminder_collection.save(reminder)
			flash( reminder["title"] + reminder["reminders"]["TAGLIANDO"] , 'danger') 


			




"""
def GetCarDataValue(CarDataValue,CaraData_id,form):
	lista = {1 : 'kmattuali.data', 2: 'dataRevisione.data', 3: 'kmTagliando.data', 4: 'dataAssicurazione.data', 5: 'dataBollo.label', 6: 'kmMedi.data'}
	for i in lista.keys():
		if CaraData_id == i:
			if i == 1 or 3 or 6:
				setattr(form, lista[i], CarDataValue.valueInt)
			elif i == 2 or 4 or 5:
				setattr(form, lista[i], CarDataValue.valueDate)
	print(form.kmattuali.data)

	
	#map(lambda item: setattr(someObject, *item), attrs.iteritems())
"""

		
		
	

