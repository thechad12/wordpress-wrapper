from migrate.versioning import api
import os.path
from config import SQLALCHEMY_DB_URI
from app import db, Base

Base.metadata.create_all(db)
if not os.path.exists(SQLALCHEMY_DB_URI):
	api.create(SQLALCHEMY_DB_URI, 'database repository')

