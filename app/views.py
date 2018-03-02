''' This file contains the main logic for the CRUD
operations of the app and their respective routes'''

from app import app, db, dbsession, login
from models import User
from forms import RegistrationForm
from flask import render_template, jsonify, redirect, url_for,\
request, make_response, flash
from flask import session as login_session
from flask_login import current_user, login_user, logout_user, login_required
import json
import random
import string
import wordpress_xmlrpc
from wordpress_xmlrpc import Client as wp
from wordpress_xmlrpc import WordPressPost, WordPressPage
from wordpress_xmlrpc.methods import posts


@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

# Login function
def check_login(url, username, password):
	user = User(wp_username=username, wp_password=password, wp_url=url)
	if user is None or not user.check_password(user.wp_password):
		flash('Invalid username or password')
		return redirect(url_for('login'))
	return wp(user.wp_url, user.wp_username, user.wp_password)


# Create anti-forgery state token
@app.route('/login')
def login():
	state = ''.join(random.choice(
		string.ascii_uppercase + string.digits)
		for x in range(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)

# Logout function
@login_required
@app.route('/logout/')
def logout():
	logout_user()
	flash("You have successfully been logged out")
	return redirect(url_for('index'))

# Register and create new user
@app.route('/register/', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(wp_username=form.wp_username.data, wp_url=form.wp_url.data,
			wp_password=form.wp_password.data)
		dbsession.add(user)
		dbsession.commit()
		flash('You have now registered')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register', form=form)


# Login with wordpress
@app.route('/wpconnect/', methods=['GET', 'POST'])
def wp_connect():
	# Check that state token is the one created on the server
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	wp_user = request.form['username']
	wp_password = request.form['password']
	user = dbsession.query(User).filter_by(wp_username=wp_user)
	check_login(user.wp_url, user.wp_username, user.wp_password)
	return redirect(url_for('get_posts'))


# Query posts of user
@app.route('/posts/')
@login_required
def get_posts():
	client = check_login(user.wp_url, user.wp_username, user.wp_password)
	wp_posts = client.call(posts.GetPosts())
	return render_template('posts.html')

# View specific post
@app.route('/posts/<int:post_id>')
@login_required
def view_post(post_id):
	client = check_login(user.wp_url, user.wp_username, user.wp_password)
	wp_post = client.call(posts.GetPost(post_id))
	return render_template('post.html')

# Create new post
@app.route('/newpost', methods=['GET', 'POST'])
@login_required
def new_post():
	client = check_login(user.wp_url, user.wp_username, user.wp_password)
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
@login_required
def edit_post(wp_post_id):
	client = check_login(user.wp_url, user.wp_username, user.wp_password)
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
@login_required
def delete_post(wp_post_id):
	client = check_login(user.wp_url, user.wp_username, user.wp_password)
	if request.method == 'POST':
		delete_wp_post = request.form['delete']
		if delete_wp_post == 'delete':
			client.call(posts.DeletePost(wp_post_id))
			flash('Post deleted successfully')
			return redirect(url_for('get_posts'))
	else:
		return render_template('deletepost.html', wp_post_id=wp_post_id)

# Show list of wordpress pages
@app.route('/pages/')
@login_required
def get_pages():
	client = check_login(user.wp_url, user.wp_username, user.wp_password)
	wp_pages = client.call(posts.GetPosts({'post_type': 'page'},
		results_class=WordPressPage))
	return render_template('pages.html')

# custom filtering functionality,
# to be shown with AJAX request
@app.route('/filterposts/', methods=['GET', 'POST'])
@login_required
def filter_posts():
	client = check_login(user.wp_url, user.wp_username, user.wp_password)
	if request.method == 'POST':
		custom_filter = request.form['filter']
		max_show = request.form['number']
		# show max if max is filled in, otherwise ignore it
		filtered_posts = client.call(posts.GetPosts({'post_type': custom_filter,
			'number': max_show})) if max_show is not None else client.call(posts.GetPosts({
			'post_type': custom_filter}))
		return filtered_posts
	else:
		return render_template('posts.html')

# Custom ordering functionality,
# to be shown with AJAX request
@app.route('/orderedposts/', methods=['GET', 'POST'])
@login_required
def order_posts():
	client = check_login(user.wp_url, user.wp_username, user.wp_password)
	if request.method == 'POST':
		date = request.form['date']
		title = request.form['title']
		order = request.form['order']
		ordered_posts = client.call(posts.GetPosts({'orderby': date, 'order': order}))
		return ordered_posts
	else:
		return render_template('posts.html')








