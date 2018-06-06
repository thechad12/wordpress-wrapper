'''This file contains logic for viewing, modifying
and deleting user profiles'''
from app.session import *
from app import app, db, dbsession, login
from app.models import User
from app.forms import EditForm
from app.session import logout
from flask import session as login_session
from flask import render_template, url_for, redirect, request, flash
from flask_session import Session
import json
from wordpress_xmlrpc import Client as wp

@app.route('/users/<int:user_id>')
def user_profile(user_id):
	user = dbsession.query(User).filter_by(id=user_id).one()
	return render_template('users/user.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
	if 'user' not in login_session:
		return redirect(url_for('index'))
	user = dbsession.query(User).filter_by(id=user_id).one()
	form = EditForm()
	if request.method == 'POST':
		user.id = user_id
		user.wp_username = form.wp_username.data
		user.wp_password = user.set_password_hash(form.wp_password.data)
		user.wp_url = form.wp_url.data
		dbsession.add(user)
		dbsession.commit()
		flash('User info edited successfully')
		return redirect(url_for('user_profile', user_id=user_id))
	return render_template('users/editprofile.html')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
	if 'user' not in login_session:
		return redirect(url_for('index'))
	user = dbsession.query(User).filter_by(id=user_id).one()
	if request.method == 'POST':
		dbsession.delete(user)
		dbsession.commit()
		# Does this make sense?
		logout(user.id)
		flash('User deleted successfully')
		return redirect(url_for('index'))
	return render_template('users/deleteprofile.html')



