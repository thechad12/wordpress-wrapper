'''This file contains the logic for logins and session
management.'''

from app import app, db, dbsession, login
from app.models import User
from app.forms import LoginForm
from flask import session as login_session
from flask import render_template, url_for, redirect, flash
from flask_login import current_user, logout_user, login_user
import json
import random
import string
from wordpress_xmlrpc import Client as wp
from werkzeug.security import check_password_hash
from simplecrypt import encrypt, decrypt

# Function to store login information in session
@login.user_loader
def load_user(user_id):
	return dbsession.query(User).filter_by(id=user_id).first()

# Login function
def check_login(url, username, password):
	user = dbsession.query(User).filter_by(wp_username=username).one()
	if not check_password_hash(user.wp_password, password):
		return render_template('error/401.html')
	else:
		return wp(url, username, password)

def get_url(username):
	user = dbsession.query(User).filter_by(wp_username=username).first()
	return user.wp_url

# Create anti-forgery state token
@app.route('/login', methods=['GET', 'POST'])
def login():
	#if login_session['logged_in'] is not None and login_session['logged_in'] == True:
	#	return redirect(url_for('get_posts'))
	print(current_user.is_authenticated)
	form = LoginForm()
	print(form.validate_on_submit)
	if form.validate_on_submit():
		user = dbsession.query(User).filter_by(wp_username=form.wp_username.data).one()
		if user is None or not user.check_password(form.wp_password.data):
			flash('Invalid login')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		check_login(user.wp_url, user.wp_username, form.wp_password.data)
		login_session['logged_in'] = True
		login_session['pw'] = form.wp_password.data
		return redirect(url_for('get_posts'))
	return render_template('users/login.html', title='Log In', form=form)


# Logout function
@app.route('/logout/')
def logout():
	user = current_user
	logout_user()
	login_session['logged_in'] = False
	flash("You have successfully been logged out")
	return redirect(url_for('index'))

# Check if user is logged in
def check_logged_in(session):
	if 'user' not in session:
		return render_template('common/index.html')

# Generate csrf token for registration and
# any other functions where it may be necessary
# in the future
def gen_csrf_token():
	csrf = ''.join(random.choice(
		string.ascii_uppercase + string.digits)
	for x in range(32))
	login_session['csrf_token'] = csrf
	return csrf

