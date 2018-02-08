from flask import Flask
import sqlalchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config.from_object('config')
# Temporary database while app is in development/testing.
# Switch to more secure database outside of app when in
# production.
db = create_engine('sqlite:///users.db')

from app import views, models