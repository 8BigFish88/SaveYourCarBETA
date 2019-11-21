from apps.appCar.models import Car, CarDataValue, CarData
from apps import db, bcrypt

def InsertCarDataValue(CarDataValue,CaraData_id,form):
	for i in range(1,7,1):
		lista = [form.kmattuali.data, form.dataRevisione.data, form.kmTagliando.data, form.dataAssicurazione.data, form.dataBollo.data, form.kmMedi.data]
		if CaraData_id == i:
			if i == 1 or 3 or 6:
				CarDataValue.valueInt = lista[i-1]
			elif i == 2 or 4 or 5:
				CarDataValue.valueDate = lista[i-1]

def GetCarDataValue(CarDataValue,CaraData_id,form):
	lista = [form.kmattuali, form.dataRevisione, form.kmTagliando, form.dataAssicurazione, form.dataBollo, form.kmMedi]
	for i in lista:
		if CaraData_id == lista.index(i)+1:
			if lista.index(i)+1 == 1 or 3 or 6:
				i.data = CarDataValue.valueInt
			elif lista.index(i)+1 == 2 or 4 or 5:
				i.data = CarDataValue.valueDate

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
		
		
	

