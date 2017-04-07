# views.py

import json
from flask import redirect, url_for, request, render_template, jsonify
from flask_cas import CAS
from dash import toJSON
from main import app
from Table import Table
from database import *

cas = CAS(app)
table = Table()

with open('secrets', 'r') as s:
	secrets = s.readlines()
	
app.secret_key = secrets[0].replace('\n', '')
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas/'
app.config['CAS_AFTER_LOGIN'] = 'index'

@app.route('/', methods = ['GET', 'POST'])
def index():
	#if not logged in. is this the correct way to do it?
	if cas.username is None or cas.token is None:
		return redirect(url_for('landing'))

	# get POSTed json
	jresponse = request.get_json()
	if jresponse is not None:
		print jresponse['netid']
		daytimes = [daytime for daytime in jresponse['response']]
		print daytimes
	
	# initial protocol
	init_data = toJSON(cas.username)
	return render_template('index.html',
							user=cas.username,
							token=cas.token,
							table=table,
							init_data=init_data)

@app.route('/landing')
def landing():
	return render_template('landing.html')