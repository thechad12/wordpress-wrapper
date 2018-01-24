from sqlalchemy import *
from app import db
import sys
from passlib.apps import custom_app_context as pass_context

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	wp_username = db.Column(db.String)
	wp_password = db.Column(db.String)

	def hash_password(self, password):
		self.password_hash = pass_context.encrypt(password)

	def verify_password(self, password):
		return pass_context.verify(password, self.password_hash)

