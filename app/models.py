from sqlalchemy import *
from app import db
import sys
from passlib.apps import custom_app_context as pass_context
from wordpress_xmlrpc import Client as wp_client


class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	wp_username = db.Column(db.String)
	wp_password = db.Column(db.String)
	wp_url = db.Column(db.String)

	def authenticate(self, url, username, password):
		wp_login = wp_client(url, username, password)
		return wp_login

