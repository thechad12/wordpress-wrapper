''' This file contains the main logic for the CRUD
operations of the app and their respective routes'''

from app import app, db, session
from models import User
from flask import render_template, jsonify, redirect, session, url_for,\
request, make_response, flash
from flask import session as login_session
import json
import random
import string
import wordpress_xmlrpc
from wordpress_xmlrpc import Client as wp
from wordpress_xmlrpc import WordPressPost
from wordpress_xmlrpc.methods import posts

@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

# Login function
def check_login(url, username, password):
	user = User(wp_username=username, wp_password=password, wp_url=url)
	login_session['user'] = user.wp_username
	login_session['password'] = user.wp_password
	login_session['url'] = user.wp_url
	return wp(user.wp_url, user.wp_username, user.wp_password)


# Create anti-forgery state token
@app.route('/login')
def login():
	state = ''.join(random.choice(
		string.ascii_uppercase + string.digits)
		for x in range(32))
	login_session['state'] = state
	print(state)
	return render_template('login.html', STATE=state)

# Logout function
@app.route('/logout')
def logout():
	session.delete(login_session)
	session.commit()
	flash("You have successfully been logged out")
	return render_template('index.html')

# Create user
def create_user(login_session):
	new_user = User(wp_username=login_session['user'],
		wp_password=login_session['password'], wp_url=login_session['url'])
	session.add(new_user)
	session.commit()
	user = session.query(User).filter_by(wp_username=login_session['user']).one()
	return user.id

# Login with wordpress
@app.route('/wpconnect', methods=['GET', 'POST'])
def wp_connect():
	# Check that state token is the one created on the server
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	#try:
	login_session['url'] = request.form['url']
	login_session['user'] = request.form['username']
	login_session['password'] = request.form['password']
	check_login(login_session['url'], login_session['user'],
		login_session['password'])
	return redirect(url_for('get_posts'))
	#except InvalidCredentialsError:
	#	response = make_response(json.dumps('Invalid login'), 401)
	#	response.headers['Content-Type'] = 'application/json'
	#	return response
	#except ServerConnectionError:
	#	response = make_response(json.dumps('Could not connect to server'), 401)
	#	response.headers['Content-Type'] = 'application/json'
	#	return response


# Query posts of user
@app.route('/posts/')
def get_posts():
	if 'user' not in login_session:
		return render_template('index.html')
	else:
		client = check_login(login_session['url'], login_session['user'],
			login_session['password'])
		wp_posts = client.call(posts.GetPosts())
		return render_template('posts.html')

# View specific post
@app.route('/posts/<int:post_id>')
def view_post(post_id):
	if 'user' not in login_session:
		return render_template('index.html')
	else:
		client = check_login(login_session['url'], login_session['user'],
			login_session['password'])
		wp_post = client.call(posts.GetPost(post_id))
	return render_template('post.html')

# Create new post
@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
	if 'user' not in login_session:
		return render_template('index.html')
	else:
		client = check_login(login_session['url'], login_session['user'],
			login_session['password'])
		if request.method == 'POST':
			new_wp_post = WordPressPost
			new_wp_post.title = request.form['title']
			new_wp_post.content = request.form['content']
			new_wp_post.id = client.call(posts.NewPost(new_wp_post))
			# Allow user to check post before publishing
			new_wp_post.status = request.form['publish']
			if new_wp_post.status == 'publish':
				client.call(posts.EditPost(new_wp_post.id, new_wp_post))
				flash('New post successfully added')
				return redirect(url_for('get_posts'))
		else:
			return render_template('newpost.html')

# Edit existing post
@app.route('/posts/<int:wp_post_id>/edit', methods=['GET', 'POST'])
def edit_post(wp_post_id):
	if 'user' not in login_session:
		return render_template('index.html')
	else:
		client = check_login(login_session['url'], login_session['user'],
			login_session['password'])
		if request.method == 'POST':
			edit_wp_post = WordPressPost
			edit_wp_post.title = request.form['title']
			edit_wp_post.content = request.form['content']
			edit_wp_post.id = wp_post_id
			# Check before publishing post
			edit_wp_post.status = request.form['publish']
			if edit_wp_post.status == 'publish':
				client.call(posts.EditPost(edit_wp_post.id, edit_wp_post))
				flash('Post edited successfully')
				return redirect(url_for('get_posts'))
		else:
			return render_template('editpost.html', wp_post_id=wp_post_id)

# Delete an existing post
@app.route('/posts/<int:wp_post_id>/delete', methods=['GET', 'POST'])
def delete_post(wp_post_id):
	if 'user' not in login_session:
		return render_template('index.html')
	else:
		client = check_login(login_session['url'], login_session['user'],
			login_session['password'])
		if request.method == 'POST':
			delete_wp_post = request.form['delete']
			if delete_wp_post == 'delete':
				client.call(posts.DeletePost(wp_post_id))
				flash('Post deleted successfully')
				return redirect(url_for('get_posts'))
		else:
			return render_template('deletepost.html', wp_post_id=wp_post_id)




