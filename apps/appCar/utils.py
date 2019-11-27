from apps.appCar.models import Car, CarDataValue, CarData
from apps import db
from datetime import datetime  
from datetime import timedelta  
from flask import flash

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
	lista = [form.kmattuali.data, form.dataRevisione.data, form.kmTagliando.data, form.dataAssicurazione.data, form.dataBollo.data, form.kmMedi.data]
	carDataValue={}
	for i in range(1,7):
		if i == 1 or 3 or 6:
			carDataValue[i] = CarDataValue(valueInt = lista[i-1], id_CarData = i, car_author = car )
			db.session.add(carDataValue[i])
		elif i == 2 or 4 or 5:
			carDataValue[i] = CarDataValue(valueDate = lista[i-1], id_CarData = i, car_author = car )
			db.session.add(carDataValue[i])

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

def FlashReminders(car,carvalues):
	kmMedi = GetKm(car, carvalues)
	rilievo = GetDateDetection(car, carvalues)
	for value in carvalues:
		if (datetime.now() >= value.valueDate - timedelta(days=30)) and (value.id_CarData == 4):   
			flash(car.name.upper() +': L\' ASSICURAZIONE di quest\' auto sta per scadere. Rinnovala!', 'danger')
		if (datetime.now() >= value.valueDate - timedelta(days=30)) and (value.id_CarData == 5):   
			flash(car.name.upper() +': Il BOLLO di quest\' auto sta per scadere. Rinnovalo!', 'danger')
		if  ((((datetime.now() - value.valueDate >= timedelta(days=730) - timedelta(days=30)) 
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
			flash(car.name.upper() +': Quest\' auto deve fare la REVISIONE. Affrettati!', 'danger')
		if ((value.id_CarData == 3) 
			and
			((rilievo[1] + (kmMedi*((datetime.now() - rilievo[0])/timedelta(days=7))))-value.valueInt > 30000)
			):
			flash(car.name.upper() +': Quest\' auto ha bisogno di un TAGLIANDO. Affrettati!', 'danger')




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

		
		
	

