# views.py

import json, db2server, server2db
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
	#if not logged in display landing page
	if cas.username is None or cas.token is None:
		return redirect(url_for('landing'))

	# if user has logged in for the first time, add user to db
	server2db.inviteUsers([cas.username])

	# get POSTed json
	jpost = request.get_json()

	# sample creation
	jpost1 = {u'category': 'creation', u'title': 'The Olympics', u'response': [{u'date': u'04-18-2017', u'time': u'4pm'}], u'netid': u'gwan', u'responders': [u'hsolis'], u'creationDate': '04-17-2017'}
	# sample response
	jpost2 = {u'category': 'response', u'mid': 10, u'response': [{u'date': u'04-19-2017', u'time': u'7am'}, {u'date': u'04-20-2017', u'time': u'7am'}], u'netid': u'hsolis'}
	# sample decision
	jpost3 = {u'category': 'decision', u'mid': 10, u'finalTime': [{u'date': u'04-22-2017', u'time': u'10am'}], u'netid': u'gwan'}
	# sample update preferred times
	jpost4 = {u'category': 'updatePref', u'preferredTimes': [{u'day': u'Mon', u'time': u'10am'}, {u'day': u'Tue', u'time': u'11am'}], u'netid': u'gwan'}
	# sample meeting deletion
	jpost5 = {u'category': 'meetingDelete', u'mid': 11, u'netid': 'gwan'}

	
	if jpost is not None:
		# test make sure received
		#jpost = jpost5
		print jpost
		# update database
		global valid
		valid = server2db.parse(jpost)
	
	# initial protocol
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