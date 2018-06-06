from sqlalchemy import *
from app import db, Base, login, dbsession
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from wordpress_xmlrpc import Client as wp
from simplecrypt import encrypt, decrypt


# Create the user class to be stored in the database

class User(UserMixin, Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	wp_username = Column(String)
	wp_password = Column(String)
	wp_url = Column(String)
	enc_password = Column(String)

	def set_password_hash(self, password):
		self.wp_password = generate_password_hash(password)
		return self.wp_password

	def check_password(self, password):
		return check_password_hash(self.wp_password, password)

	def set_encrypted_password(self, password):
		self.enc_password = encrypt(password, password)

	def get_encrypted_password(self, password):
		return decrypt(password, password)

	def __repr__(self):
		return '<User {}/><Password {}/><URL {}'.format(self.wp_username,
			self.wp_password, self.wp_url)









