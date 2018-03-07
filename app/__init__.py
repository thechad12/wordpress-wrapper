from flask import Flask
from flask_login import LoginManager
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_htmlmin import HTMLMIN

app = Flask(__name__)
app.config.from_object('config')
login = LoginManager(app)
login.login_view = 'login'
app.config('MINIFY_PAGE') = True
HTMLMIN(app)
# Temporary database while app is in development/testing.
# Switch to more secure database outside of app when in
# production.
db_uri = 'sqlite:///users.db'
db = create_engine(db_uri)
Base = declarative_base()
DBSession = sessionmaker(bind=db)
dbsession = DBSession()


from app import views, models, session
from models import User
from session import *

