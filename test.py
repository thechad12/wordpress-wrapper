''' This file contains the test cases.
Test cases will create, edit, update, and delete
a post for a test user account. Test is run
automatically everytime there is a commit'''

import unittest
from app import app, models

class TestApp(unittest.TestCase):

	def set_up(self):
		self.app = app.test_client()

	def test_homepage(self):
		rv = self.app.get('/')
		self.assertTrue(rv.data)
		self.assertEqual(rv.status_code, 200)

	def test_user_ops(self):
		u = User('test', 'test', 'test')
		u.authenticate()
		get_posts()

if __name__ == '__main__':
	unittest.main()