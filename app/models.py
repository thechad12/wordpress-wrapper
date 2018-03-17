from sqlalchemy import *
from app import db, Base, login
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from wordpress_xmlrpc import Client as wp


# Create the user class to be stored in the database

class User(UserMixin, Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	wp_username = Column(String)
	wp_password = Column(String)
	wp_url = Column(String)

	def authenticate(self, url, username, password):
		wp_login = wp(url, username, password)
		return wp_login

	def set_password_hash(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password(self.password_hash, password)


# Function to store login information in session
@login.user_loader
def load_user(user_id):
	return db.session.query(User).filter_by(id=user_id).one()




