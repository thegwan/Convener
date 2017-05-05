# views.py
# yses Flask-CAS: https://github.com/cameronbwhite/Flask-CAS

import json, db2server, server2db, autoDb
from flask import redirect, url_for, request, render_template, jsonify
from flask_cas import CAS
from main import app
from Table import Table
from Table_Pref import Table_Pref

cas = CAS(app)
table = Table()
table_pref = Table_Pref()

with open('secrets', 'r') as s:
	secrets = s.readlines()
	
app.secret_key = secrets[0].replace('\n', '')
app.config['CAS_SERVER'] = 'https://fed.princeton.edu/cas/'
app.config['CAS_AFTER_LOGIN'] = 'index'
valid = False;

@app.route('/_refreshPage/', methods = ['GET'])
def refreshPage():
	init_data = json.dumps(db2server.init_protocol(cas.username))
	return init_data

@app.route('/_creationError/', methods = ['GET'])
def creationError():
	global valid
	return json.dumps(valid)

@app.route('/', methods = ['GET', 'POST'])
def index():
	#if not logged in, display landing page
	if cas.username is None or cas.token is None:
		return redirect(url_for('landing'))

	# if user has logged in for the first time, add user to db
	server2db.inviteUsers([cas.username])

	# get POSTed json
	jpost = request.get_json()
	if jpost is not None:
		global valid
		valid = server2db.parse(jpost)
	
	# initial protocol
	autoDb.delete_expired_meetings()
	init_data = json.dumps(db2server.init_protocol(cas.username))

	# ------------------------------------------------------------------------------------------

	return render_template('index.html',
							user=cas.username,
							token=cas.token,
							table=table,
							table_pref=table_pref,
							init_data=init_data)

@app.route('/landing')
def landing():
	return render_template('landing.html')