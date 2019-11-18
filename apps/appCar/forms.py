from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apps.appCar.models import Car

class CarForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    fuel = StringField('Alimentazione', validators=[DataRequired()])
    matriculation = DateField('Data immatricolazione (aa-mm-gg)', validators=[DataRequired()])
    kmattuali = StringField('Km attuali', validators=[DataRequired()])
    dataRevisione = DateField('Data ultima revisione (aa-mm-gg)', validators=[DataRequired()])
    submit = SubmitField('Submit')
