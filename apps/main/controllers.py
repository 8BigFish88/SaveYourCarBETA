from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
	if current_user.is_authenticated:
		return redirect(url_for('cars.auto'))
	else:
		return render_template('home.html', title='Home Page')
  
