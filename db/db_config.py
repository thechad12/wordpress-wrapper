import os
import psycopg2
from app import *


# Try connection to database url (configured in heroku)
# connect to sqlite db if running locally
try:
	SQLALCHEMY_DB_URI = os.environ['DATABASE_URL']
	conn = psycopg2.connect(SQLALCHEMY_DB_URI, sslmode='require')
except KeyError:
	SQLALCHEMY_DB_URI = 'sqlite:///users.db'