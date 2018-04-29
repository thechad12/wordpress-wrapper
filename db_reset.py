from app import db, dbsession
import os.path
import sys
from config import SQLALCHEMY_DB_URI
from app.models import User

if not os.path.exists(SQLALCHEMY_DB_URI):
	pass
# Check if on production or staging environment,
# where a DB reset should not be accessible
elif os.environ.get('HEROKU') is None:
	dbsession.query(User).delete()
else:
	pass
