from app import app, db
from models import User
from flask import render_template, jsonify, redirect, session, url_for,\
request, make_response
import json

@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')