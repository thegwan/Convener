# views.py

import json, dash
from flask import redirect, url_for, request, render_template, jsonify
from flask_cas import CAS
from main import app
from Table import Table

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
	# init_data = json.dumps(toJSON(cas.username))

	# sample test data to connect to front end
	# ------------------------------------------------------------------------------------------
	init_data = json.dumps{
						  "confirmed": [
						    {
						      "creator": "hsolis", 
						      "mine": true, 
						      "times": [
						        [
						          {
						            "Day": "Thu", 
						            "Time": "8:30"
						          }, 
						          {
						            "Day": "Fri", 
						            "Time": "12:00"
						          }
						        ]
						      ], 
						      "title": "Colonial Lunch"
						    }
						  ], 
						  "my_meetings": [
						    {
						      "all_responded": false, 
						      "nresp_netids": [
						        "gwan"
						      ], 
						      "resp_netids": [
						        "hsolis"
						      ], 
						      "times": [
						        {
						          "Day": "Fri", 
						          "Time": "12:00"
						        }
						      ], 
						      "title": "Back Massage"
						    }, 
						    {
						      "all_responded": true, 
						      "nresp_netids": [], 
						      "resp_netids": [
						        "hsolis", 
						        "gwan", 
						        "ksha"
						      ], 
						      "times": [
						        {
						          "Day": "Thu", 
						          "Time": "8:30"
						        }, 
						        {
						          "Day": "Fri", 
						          "Time": "12:00"
						        }, 
						        {
						          "Day": "Thu", 
						          "Time": "8:30"
						        }, 
						        {
						          "Day": "Fri", 
						          "Time": "12:00"
						        }, 
						        {
						          "Day": "Fri", 
						          "Time": "12:00"
						        }
						      ], 
						      "title": "Colonial Lunch"
						    }
						  ], 
						  "my_requests": [
						    {
						      "creator": "gwan", 
						      "title": "Charter Friday"
						    }, 
						    {
						      "creator": "kl9", 
						      "title": "Code@Night"
						    }
						  ], 
						  "pending": [
						    {
						      "creator": "hsolis", 
						      "mine": true, 
						      "times": [
						        [
						          {
						            "Day": "Fri", 
						            "Time": "12:00"
						          }
						        ]
						      ], 
						      "title": "Back Massage"
						    }, 
						    {
						      "creator": "kl9", 
						      "mine": false, 
						      "times": [
						        [
						          {
						            "Day": "Fri", 
						            "Time": "20:00"
						          }
						        ]
						      ], 
						      "title": "Code@Night"
						    }
						  ]
						}

	# ------------------------------------------------------------------------------------------

	return render_template('index.html',
							user=cas.username,
							token=cas.token,
							table=table,
							init_data=init_data)

@app.route('/landing')
def landing():
	return render_template('landing.html')