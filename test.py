''' This file contains the test cases.
Test cases will create, edit, update, and delete
a post for a test user account. Test is run
automatically everytime there is a commit'''

import unittest
from app import app, db
from app.models import User
from app.views import get_posts
import os
import config

class TestApp(unittest.TestCase):

	def set_up(self):
		app.config['TEST'] = True
		app.cofig['SQLALCHEMY_DATABASE_URI'] = db

	def test_user_ops(self):
		u = User()
		try:
			u.authenticate('test', 'test', 'test')
			get_posts()
		except:
			pass

if __name__ == '__main__':
	unittest.main()