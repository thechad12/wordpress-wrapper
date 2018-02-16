from sqlalchemy import *
from app import db, Base
import sys
from passlib.apps import custom_app_context as pass_context
from wordpress_xmlrpc import Client as wp


# Create the user class to be stored in the database

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	wp_username = Column(String)
	wp_password = Column(String)
	wp_url = Column(String)

	def authenticate(self, url, username, password):
		wp_login = wp(url, username, password)
		return wp_login

	def hash_password(self, password):
		self.password_hash = pass_context.encrypt(password)

	def verify_password(self, password):
		return pass_context.verify(password, self.password_hash)


