from flask import Flask
from flask_login import LoginManager
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object('config')
login = LoginManager(app)
login.login_view = 'login'
# Temporary database while app is in development/testing.
# Switch to more secure database outside of app when in
# production.
db = create_engine('sqlite:///users.db')
Base = declarative_base()
DBSession = sessionmaker(bind=db)
dbsession = DBSession()

from app import views, models
from models import User