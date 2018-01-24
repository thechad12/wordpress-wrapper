from flask import Flask
import sqlalchemy

app = Flask(__name__)
app.config.from_object('config')
db = create_engine('sqlite:///users.db')

from app import views, models