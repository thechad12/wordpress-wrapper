''' This file contains the main logic for the CRUD
operations of the app and their respective routes'''

from app import app, db, dbsession, login
from app.models import User, SpecialTransport
from app.session import *
from app.profile import *
from app.forms import RegistrationForm
from flask import render_template, jsonify, redirect, url_for,\
request, make_response, flash, abort
from flask import session as login_session
from flask_login import current_user, login_user, logout_user, login_required
import json
import random
import string
import wordpress_xmlrpc
from wordpress_xmlrpc import Client as wp
from wordpress_xmlrpc import WordPressPost, WordPressPage
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from simplecrypt import encrypt, decrypt


@app.route('/')
@app.route('/home')
def index():
 	return render_template('common/index.html',login_session=login_session,current_user=current_user)

@app.errorhandler(404)
def not_found(error):
	return render_template('error/404.html'), 404

@app.errorhandler(500)
def server_error(error):
	return render_template('error/500.html'), 500

# For client functions to work, wordpress
# URL must point to /xmlrpc.php
# function to check if that is in URL,
# appends it if not
def check_url(url):
	if '/xmlrpc.php' not in url:
		url += '/xmlrpc.php'
	return url

# Register and create new user
@app.route('/register', methods=['GET', 'POST'])
def register():
	#if current_user.is_authenticated:
	#	return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(wp_username=form.wp_username.data, wp_url=form.wp_url.data,
			wp_password=generate_password_hash(form.wp_password.data))
		dbsession.add(user)
		dbsession.commit()
		flash('You have now registered')
		return redirect(url_for('login'))
	return render_template('users/register.html',title='Register', form=form)

# Query posts of user
@login_required
@app.route('/posts/')
def get_posts():
	user = current_user
	client = check_login(user.wp_url, user.wp_username,
		login_session['pw'])
	wp_posts = client.call(posts.GetPosts())
	return render_template('posts/posts.html', wp_posts=wp_posts)

# View specific post
@login_required
@app.route('/posts/<int:post_id>')
def view_post(post_id):
	user = current_user
	client = check_login(user.wp_url, user.wp_username,
			login_session['pw'])
	wp_post = client.call(posts.GetPost(post_id))
	return render_template('posts/post.html', post=wp_post)

# Create new post
@login_required
@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
	user = current_user
	client = check_login(user.wp_url, user.wp_username,
		login_session['pw'])
	if request.method == 'POST':
		new_wp_post = WordPressPost()
		new_wp_post.title = request.form['title']
		new_wp_post.content = request.form['content']
		new_wp_post.status = 'publish'
		new_wp_post.id = client.call(posts.NewPost(new_wp_post))
		flash('New post successfully added')
		return redirect(url_for('get_posts'))
	else:
		return render_template('posts/newpost.html')

# Edit existing post
@login_required
@app.route('/posts/<int:wp_post_id>/edit', methods=['GET', 'POST'])
def edit_post(wp_post_id):
	user = current_user
	client = check_login(user.wp_url, user.wp_username,
		login_session['pw'])
	if request.method == 'POST':
		edit_wp_post = WordPressPost()
		edit_wp_post.title = request.form['title']
		edit_wp_post.content = request.form['content']
		edit_wp_post.id = wp_post_id
		edit_wp_post.status = 'publish'
		client.call(posts.EditPost(edit_wp_post.id, edit_wp_post))
		flash('Post edited successfully')
		return redirect(url_for('get_posts'))
	else:
		return render_template('posts/editpost.html', wp_post_id=wp_post_id)

# Delete an existing post
@login_required
@app.route('/posts/<int:wp_post_id>/delete', methods=['GET', 'POST'])
def delete_post(wp_post_id):
	user = current_user
	client = check_login(user.wp_url, user.wp_username,
		login_session['pw'])
	wp_post = client.call(posts.GetPost(wp_post_id))
	if request.method == 'POST':
		client.call(posts.DeletePost(wp_post_id))
		flash('Post deleted successfully')
		return redirect(url_for('get_posts'))
	else:
		return render_template('posts/deletepost.html', wp_post_id=wp_post_id, post=wp_post)

# Show list of wordpress pages
@login_required
@app.route('/pages/')
def get_pages():
	check_logged_in(login_session)
	client = check_login(user.wp_url, user.wp_username,
		login_session['pw'])
	wp_pages = client.call(posts.GetPosts({'post_type': 'page'},
		results_class=WordPressPage))
	return render_template('posts/pages.html')

# Upload image to directory
@login_required
@app.route('/upload')
def upload_image():
	user = current_user
	client = check_login(user.wp_url, user.wp_username,
		login_session['pw'])
	form = ImageUpload()
	if form.validate_on_submit():
		image_data = form.image.data
		filename = secure_filename(image_data.filename)
		wp_image_data = {
			'name': filename,
			'type': 'image/jpeg'
		}
		with open(filename, 'rb') as img:
			data['bits'] = xmlrpc_client.Binary(img.read())
		res = client.call(media.UploadFile(data))
		return redirect(url_for('get_posts'))
	return render_template('templates/files/upload.html')


# custom filtering functionality,
# to be shown with AJAX request
@app.route('/filterposts/', methods=['GET', 'POST'])
def filter_posts():
	user = current_user
	client = check_login(user.wp_url, user.wp_username,
		login_session['pw'])
	if request.method == 'POST':
		custom_filter = request.form['filter']
		max_show = request.form['number']
		# show max if max is filled in, otherwise ignore it
		filtered_posts = client.call(posts.GetPosts({'post_type': custom_filter,
			'number': max_show})) if max_show is not None else client.call(posts.GetPosts({
			'post_type': custom_filter}))
		return filtered_posts
	else:
		return render_template('posts/posts.html')

# Custom ordering functionality,
# to be shown with AJAX request
@app.route('/orderedposts/', methods=['GET', 'POST'])
def order_posts():
	user = current_user
	client = check_login(user.wp_url, user.wp_username,
		login_session['pw'])
	if request.method == 'POST':
		date = request.form['date']
		title = request.form['title']
		order = request.form['order']
		ordered_posts = client.call(posts.GetPosts({'orderby': date, 'order': order}))
		return ordered_posts
	else:
		return render_template('posts/posts.html')








