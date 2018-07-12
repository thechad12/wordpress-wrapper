from flask import Flask
from flask_login import LoginManager
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)
app.config.from_object('config')
login = LoginManager(app)
login.login_view = 'wp_connect'
app.config['MINIFY_PAGE'] = True
# Check if DB URL is configured (will be in heroku environment for psql)
# if not, connect to local sqlite db in memory
try:
	db_uri = os.environ['DATABASE_URL']
except KeyError:
	db_uri = 'sqlite:///users.db'
db = create_engine(db_uri)
Base = declarative_base()
DBSession = sessionmaker(bind=db)
dbsession = DBSession()
migrate = Migrate(app, db)


from app import views, models, session
from app.models import User
from app.session import *

