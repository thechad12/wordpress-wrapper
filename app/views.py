from app import app, db
from models import User
from flask import render_template, jsonify, redirect, session, url_for,\
request, make_response
import json
import random
import string
from wordpress_xmlrpc import InvalidCredentialsError, Client
from wordpress_xmlrpc.methods import posts

@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

def check_login(url, username, password):
	user = User(wp_username=username, wp_password=password, wp_url=url)
	if user.authenticate is InvalidCredentialsError:
		return False
	else:
		login_session['user'] = user.wp_username
		login_session['password'] = user.wp_password
		login_session['url'] = user.wp_url
		return True

# Create anti-forgery state token
@app.route('/login')
def login():
	state = ''.join(random.choice(
		string.ascii_uppercase + string.digits)
	for x in range(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)

# Query posts of user
@app.route('/posts/')
def get_posts():
	if 'user' not in login_session:
		return render_template('index.html')
	else:
		client = check_login(login_session['username'], login_session['password'],
			login_session['url'])
		wp_posts = client.call(posts.GetPosts())
		return render_template('posts.html')


