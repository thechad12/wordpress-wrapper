from app import *
import os
import psycopg2
app.secret_key = 'secret_key_will_be_set'

if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	try:
		file_handler = RotatingFileHandler('tmp/wordpress.log', 'a',
			1*1024*1024, 10)
		file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:\
			%(message)s [in %(pathname)s:%(lineo)d]'))
		app.logger.setLevel(logging.INFO)
		file_handler.setLevel(logging.INFO)
		app.logger.info('app log')
	except IOError:
		pass

# Try connection to database url (configured in heroku)
# connect to sqlite db if running locally
try:
	SQLALCHEMY_DB_URI = os.environ['DATABASE_URL']
	conn = psycopg2.connect(SQLALCHEMY_DB_URI, sslmode='require')
except KeyError:
	SQLALCHEMY_DB_URI = 'sqlite:///users.db'


