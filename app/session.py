'''This file contains the logic for logins and session
management.'''

from app import app, db, dbsession, login
from models import User
from flask import session as login_session
from flask import render_template, url_for, redirect
from flask_login import current_user
import json
import random
import string
from wordpress_xmlrpc import Client as wp
from werkzeug.security import check_password_hash

# Function to store login information in session
@login.user_loader
def load_user(user_id):
	return dbsession.query(User).filter_by(id=user_id).one()

# Login function
def check_login(url, username, password):
	user = dbsession.query(User).filter_by(wp_username=username).one()
	if not check_password_hash(user.wp_password, password):
		return render_template('error/401.html')
	else:
		login_session['user'] = user.wp_username
		login_session['password'] = user.wp_password
		login_session['url'] = user.wp_url
		return wp(user.wp_url, user.wp_username, user.wp_password)

def get_url(username):
	user = dbsession.query(User).filter_by(wp_username=username).first()
	return user.wp_url

# Create anti-forgery state token
@app.route('/login')
def login():
	if current_user.is_authenticated:
		return redirect(url_for('get_posts'))
	state = ''.join(random.choice(
		string.ascii_uppercase + string.digits)
		for x in range(32))
	login_session['state'] = state
	return render_template('users/login.html', STATE=state)

# Logout function
@app.route('/logout/')
def logout():
	user = current_user
	logout_user()
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

