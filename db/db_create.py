from migrate.versioning import api
import os.path
from app import db, Base
import sys
from db_config import SQLALCHEMY_DB_URI

Base.metadata.create_all(db)
if not os.path.exists(SQLALCHEMY_DB_URI):
	api.create(SQLALCHEMY_DB_URI, 'database repository')

