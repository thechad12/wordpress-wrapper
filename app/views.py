from app import app, db
from models import User
from flask import render_template, jsonify, redirect, session, url_for,\
request, make_response
import json
from wordpress_xmlrpc import InvalidCredentialsError

@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

def check_login(url, username, password):
	user = User(wp_username=username, wp_password=password, wp_url=url)
	if user.authenticate is InvalidCredentialsError:
		return False
	return True

@app.route('/login')
def login():
	return render_template('login.html')