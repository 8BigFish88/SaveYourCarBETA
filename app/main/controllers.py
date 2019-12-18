from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
import logging
from app.settings.loggings.messages import Log
log = Log()

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	if current_user.is_authenticated:
		logging.info('%s'%log.loginHome)
		return redirect(url_for('cars.auto'))
	else:
		logging.info('%s'%log.logoutHome)
		return render_template('home.html', title='Home Page')
  
