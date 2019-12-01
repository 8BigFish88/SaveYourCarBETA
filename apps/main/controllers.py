from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
import logging

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	if current_user.is_authenticated:
		logging.info('Aperta pagina Home per utente autenticato')
		return redirect(url_for('cars.auto'))
	else:
		logging.info('Aperta pagina Home per utente non autenticato')
		return render_template('home.html', title='Home Page')
  
