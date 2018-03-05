''' This file contains the main logic for the CRUD
operations of the app and their respective routes'''

from app import app, db, dbsession, login
from models import User
from session import *
from forms import RegistrationForm
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
from wordpress_xmlrpc.methods import posts


@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

# Server error handling
@app.errorhandler(404)
def not_found(error):
	return render_template('error/404.html'), 404

@app.errorhandler(500)
def server_error(error):
	return render_template('error/500.html'), 500

# Register and create new user
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	csrf = gen_csrf_token()
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(wp_username=form.wp_username.data, wp_url=form.wp_url.data,
			wp_password=form.wp_password.data)
		dbsession.add(user)
		dbsession.commit()
		flash('You have now registered')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register', form=form,
		token=csrf)


# Login with wordpress
@app.route('/wpconnect/', methods=['GET', 'POST'])
def wp_connect():
	# Check that state token is the one created on the server
	if request.args.get('state') != login_session['state']:
		abort(403)
	login_session['user'] = request.form['username']
	login_session['password'] = request.form['password']
	login_session['url'] = get_url(login_session['user'])
	check_login(login_session['url'], login_session['user'],
	login_session['password'])
	return redirect(url_for('get_posts'))


# Query posts of user
@app.route('/posts/')
def get_posts():
	check_logged_in(login_session)
	client = check_login(login_session['url'], login_session['user'],
		login_session['password'])
	wp_posts = client.call(posts.GetPosts())
	return render_template('posts.html', wp_posts=wp_posts)

# View specific post
@app.route('/posts/<int:post_id>')
def view_post(post_id):
	check_logged_in(login_session)
	client = check_login(login_session['url'], login_session['user'],
			login_session['password'])
	wp_post = client.call(posts.GetPost(post_id))
	return render_template('post.html', post=wp_post)

# Create new post
@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
	check_logged_in(login_session)
	client = check_login(login_session['url'], login_session['user'],
		login_session['password'])
	if request.method == 'POST':
		new_wp_post = WordPressPost()
		new_wp_post.title = request.form['title']
		new_wp_post.content = request.form['content']
		new_wp_post.id = client.call(posts.NewPost(new_wp_post))
		# Allow user to check post before publishing
		new_wp_post.status = 'publish'
		flash('New post successfully added')
		return redirect(url_for('get_posts'))
	else:
		return render_template('newpost.html')

# Edit existing post
@app.route('/posts/<int:wp_post_id>/edit', methods=['GET', 'POST'])
def edit_post(wp_post_id):
	check_logged_in(login_session)
	client = check_login(login_session['url'], login_session['user'],
		login_session['password'])
	if request.method == 'POST':
		edit_wp_post = WordPressPost()
		edit_wp_post.title = request.form['title']
		edit_wp_post.content = request.form['content']
		edit_wp_post.id = wp_post_id
		client.call(posts.EditPost(edit_wp_post.id, edit_wp_post))
		flash('Post edited successfully')
		return redirect(url_for('get_posts'))
	else:
		return render_template('editpost.html', wp_post_id=wp_post_id)

# Delete an existing post
@app.route('/posts/<int:wp_post_id>/delete', methods=['GET', 'POST'])
def delete_post(wp_post_id):
	check_logged_in(login_session)
	client = check_login(login_session['url'], login_session['user'],
		login_session['password'])
	wp_post = client.call(posts.GetPost(wp_post_id))
	if request.method == 'POST':
		client.call(posts.DeletePost(wp_post_id))
		flash('Post deleted successfully')
		return redirect(url_for('get_posts'))
	else:
		return render_template('deletepost.html', wp_post_id=wp_post_id, post=wp_post)

# Show list of wordpress pages
@app.route('/pages/')
def get_pages():
	check_logged_in(login_session)
	client = check_login(login_session['url'], login_session['user'],
		login_session['password'])
	wp_pages = client.call(posts.GetPosts({'post_type': 'page'},
		results_class=WordPressPage))
	return render_template('pages.html')

# custom filtering functionality,
# to be shown with AJAX request
@app.route('/filterposts/', methods=['GET', 'POST'])
def filter_posts():
	check_logged_in(login_session)
	client = check_login(login_session['url'], login_session['user'],
		login_session['password'])
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
def order_posts():
	check_logged_in(login_session)
	client = check_login(login_session['url'], login_session['user'],
		login_session['password'])
	if request.method == 'POST':
		date = request.form['date']
		title = request.form['title']
		order = request.form['order']
		ordered_posts = client.call(posts.GetPosts({'orderby': date, 'order': order}))
		return ordered_posts
	else:
		return render_template('posts.html')








