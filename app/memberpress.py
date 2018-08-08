'''This file contains the functionality for memberpress
for continuous development'''

from app import app, db, dbsession, login
from app.models import User
from app.session import *
from app.profile import *
from app.forms import RegistrationForm
from flask import render_template, jsonify, redirect, \
url_for, request, make_response, flash, abort
from flask import session as login_session
