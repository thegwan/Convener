# views.py

import json, db2server, server2db
from flask import redirect, url_for, request, render_template, jsonify
from flask_cas import CAS
from main import app
from Table import Table
from GetMeetings import GetMeetings

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

	# get POSTed json (either a creation or a response)
	jpost = request.get_json()
	if jpost is not None:
		# test make sure received
		# print jpost
		# update database
		server2db.parse(jpost)
	
	# initial protocol
	init_data = json.dumps(db2server.init_protocol(cas.username))

	# sample test data to connect to front end
	# ------------------------------------------------------------------------------------------
	# init_data = json.dumps(
	# 					  {"confirmed": [
	# 					    {
	# 					      "creator": "hsolis",
	# 					      "mid":  1,
	# 					      "mine": True, 
	# 					      "times": [
	# 					          {
	# 					            "day": "Thu", 
	# 					            "time": "8pm"
	# 					          }, 
	# 					          {
	# 					            "day": "Fri", 
	# 					            "time": "12pm"
	# 					          }
	# 					      ], 
	# 					      "title": "Colonial Lunch"
	# 					    }
	# 					  ], 
	# 					  "my_meetings": [
	# 					    {
	# 					      "all_responded": False, 
	# 					      "mid": 2,
	# 					      "nresp_netids": [
	# 					        "gwan"
	# 					      ], 
	# 					      "resp_netids": [
	# 					        "hsolis"
	# 					      ], 
	# 					      "times": [
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }
	# 					      ], 
	# 					      "title": "Back Massage"
	# 					    }, 
	# 					    {
	# 					      "all_responded": True, 
	# 					      "mid": 1,
	# 					      "nresp_netids": [], 
	# 					      "resp_netids": [
	# 					        "hsolis", 
	# 					        "gwan", 
	# 					        "ksha"
	# 					      ], 
	# 					      "times": [
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "8pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "8pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }
	# 					      ], 
	# 					      "title": "Colonial Lunch"
	# 					    }
	# 					  ], 
	# 					  "my_requests": [
	# 					    {
	# 					      "creator": "gwan",
	# 					      "mid": 3, 
	# 					      "title": "Charter Friday"
	# 					    }, 
	# 					    {
	# 					      "creator": "kl9", 
	# 					      "mid": 4,
	# 					      "title": "Code@Night"
	# 					    }
	# 					  ], 
	# 					  "pending": [
	# 					    {
	# 					      "creator": "hsolis",
	# 					      "mid": 2, 
	# 					      "mine": True, 
	# 					      "times": [
	# 					          {
	# 					            "day": "Fri", 
	# 					            "time": "12pm"
	# 					          }
	# 					      ], 
	# 					      "title": "Back Massage"
	# 					    }, 
	# 					    {
	# 					      "creator": "kl9", 
	# 					      "mid": 4,
	# 					      "mine": False, 
	# 					      "times": [
	# 					          {
	# 					            "day": "Fri", 
	# 					            "time": "8pm"
	# 					          }
	# 					      ], 
	# 					      "title": "Code@Night"
	# 					    }
	# 					  ]
	# 					})
	
	# GetMeetings object to parse init_data
	#meetings = GetMeetings(init_data)

	# ------------------------------------------------------------------------------------------

	return render_template('index.html',
							user=cas.username,
							token=cas.token,
							table=table,
							#meetings=meetings,
							init_data=init_data)

@app.route('/landing')
def landing():
	return render_template('landing.html')