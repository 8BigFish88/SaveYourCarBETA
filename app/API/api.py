from flask import jsonify, request
from flask_restplus import Resource, reqparse, inputs
from app.users.models import User, UserSchema
from app.cars.models import Car, CarData, CarDataValue, CarSchema, CarDataSchema, CarDataValueSchema
from app import api
from werkzeug.datastructures import FileStorage
from flask_wtf.file import FileField

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.users.models import User
from app.cars.models import Car, CarData, CarDataValue
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from app.users.utils import save_picture, send_reset_email
from app.settings.messages import Flash,Error
from app.settings.loggings.messages import Log
import logging
flashM=Flash()
errorM=Error()
log=Log()

user_schema = UserSchema()
users_schema = UserSchema(many=True)

"""
parserPost = reqparse.RequestParser()
parserPost.add_argument('username',type=str, required=True,
help="This field cannot be blank!")
parserPost.add_argument('email',type=str, required=False)
parserPost.add_argument('avatar',type=str, required=False)
parserPost.add_argument('description',type=str, required=False)
"""
parserPost = reqparse.RequestParser(bundle_errors=True)
parserPost.add_argument('username',type=str, required=True,
help="This field cannot be blank!")
parserPost.add_argument('email',type=RegistrationForm.email, required=False)
parserPost.add_argument('password',type=str, required=False)

parserId = reqparse.RequestParser()
parserId.add_argument('user_id',type=int, required=True,
help="This field cannot be blank!")

parserPut = reqparse.RequestParser()
parserPut.add_argument('user_id',type=int, required=True,
help="This field cannot be blank!")
parserPut.add_argument('username',type=str, required=False)
parserPut.add_argument('image_file',type=UpdateAccountForm.picture, required=False)
parserPut.add_argument('email',type=str, required=False)

@api.route('/api/v1.0/users')
class GET_Users(Resource):
    def get(self):
        users = User.query.order_by(User.username).all()
        return jsonify(users_schema.dump(users))

@api.route('/api/v1.0/user')
class POST_Register_User(Resource):
    @api.expect(parserPost)
    def post(self):
        hashed_password = bcrypt.generate_password_hash(request.args.get('password')).decode('utf-8')
        user = User(
        username=request.args.get('username'),
        email=request.args.get('email'),
        password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify(user_schema.dump(user))

    @api.expect(parserId)
    def get(self):
        user_id=request.args.get('user_id')
        user = User.query.get_or_404(user_id)
        if not user:
            abort(404)
        return jsonify(user_schema.dump(user))

    @api.expect(parserId)
    def delete(self):
        user_id=request.args.get('user_id')
        user = User.query.get_or_404(user_id)
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'result': True})

    @api.expect(parserPut)
    def put(self):
        user_id=request.args.get('user_id')
        user = User.query.get_or_404(user_id)
        if not user:
            abort(404)
        user.name = request.args.get('username') if request.args.get('username') else user.username
        user.image_file =  save_picture(request.args.get('image_file')) if request.args.get('image_file') else user.image_file
        user.email =  request.args.get('email') if request.args.get('email') else user.email
        db.session.commit()
        return jsonify(user_schema.dump(user))


"""
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('%s'%flashM.userErrorLogin, 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('%s'%flashM.userAccountUpdated, 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('%s'%flashM.userResetPasswordMail, 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('%s'%flashM.userExpiredToken, 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('%s'%flashM.userPasswordUpdated, 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
"""

