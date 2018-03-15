from app import *
from raven.contrib.flask import Sentry
import os
app.secret_key = 'secret_key_will_be_set'

sentry = Sentry(app, dsn='https://60bf204801414f0eacb8edfae91cf5a0:3464b879dc744a56bbc67f963e706384@sentry.io/304772')

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

SQLALCHEMY_DB_URI = 'sqlite:///users.db'


