from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.cars.models import Car

class CarForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    fuel = RadioField('Alimentazione', choices = [('Benzina','Benzina'),('Diesel','Diesel'),('GPL','GPL')], validators=[DataRequired()])
    matriculation = DateField('Data immatricolazione (aa-mm-gg)', validators=[DataRequired()])
    kmattuali = IntegerField('Km attuali', validators=[DataRequired()])
    dataRevisione = DateField('Data ultima revisione (aa-mm-gg)', validators=[DataRequired()])
    kmTagliando = IntegerField('Km ultimo Tagliando', validators=[DataRequired()])
    dataAssicurazione = DateField('Scadenza Assicurazione (aa-mm-gg)', validators=[DataRequired()])
    dataBollo = DateField('Scadenza Bollo (aa-mm-gg)', validators=[DataRequired()])
    kmMedi = IntegerField('Km medi settimanali', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PictureForm(FlaskForm):
    picture = FileField('Update Car Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

    