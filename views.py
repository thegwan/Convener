# views.py

import json, db2server, server2db
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

@app.route('/_refreshPage/', methods = ['GET'])
def refreshPage():
	init_data = json.dumps(db2server.init_protocol(cas.username))
	return init_data

@app.route('/', methods = ['GET', 'POST'])
def index():
	#if not logged in display landing page
	if cas.username is None or cas.token is None:
		return redirect(url_for('landing'))

	# if user has logged in for the first time, add user to db
	server2db.inviteUsers([cas.username])

	# get POSTed json (either a creation or a response)
	jpost = request.get_json()
	if jpost is not None:
		# test make sure received
		# print jpost
		# update database
		server2db.parse(jpost)
	
	# initial protocol
	init_data = json.dumps(db2server.init_protocol(cas.username))
	print json.dumps(db2server.init_protocol("hsolis"), indent=2, sort_keys=True)

	# new sample test data -- look at the format
	init_data = json.dumps(
							{
						  "my_meetings": [
						    {
						      "all_responded": False, 
						      "creation_date": "Thu", 
						      "finaltime": [], 
						      "mid": 2, 
						      "nresp_netids": [
						        "gwan"
						      ], 
						      "resp_netids": [
						        "hsolis"
						      ], 
						      "responder_times": {
						        "hsolis": [
						          {
						            "date": "Fri", 
						            "time": "12pm"
						          }
						        ]
						      }, 
						      "title": "Back Massage"
						    }, 
						    {
						      "all_responded": True, 
						      "creation_date": "Thu", 
						      "finaltime": [
						        {
						          "date": "Fri", 
						          "time": "12pm"
						        }
						      ], 
						      "mid": 1, 
						      "nresp_netids": [], 
						      "resp_netids": [
						        "hsolis", 
						        "gwan", 
						        "ksha"
						      ], 
						      "responder_times": {
						        "gwan": [
						          {
						            "date": "Thu", 
						            "time": "8pm"
						          }, 
						          {
						            "date": "Fri", 
						            "time": "12pm"
						          }
						        ], 
						        "hsolis": [
						          {
						            "date": "Thu", 
						            "time": "8pm"
						          }, 
						          {
						            "date": "Fri", 
						            "time": "12pm"
						          }
						        ], 
						        "ksha": [
						          {
						            "date": "Fri", 
						            "time": "12pm"
						          }
						        ]
						      }, 
						      "title": "Colonial Lunch"
						    }
						  ], 
						  "my_preferred": [{"date": "Fri", "time": "12pm"}], 
						  "my_requests": [
						    {
						      "creation_date": "Thu", 
						      "creator": "gwan", 
						      "mid": 6, 
						      "times": [
						        {
						          "date": "Mon", 
						          "time": "3pm"
						        }, 
						        {
						          "date": "Mon", 
						          "time": "9am"
						        }
						      ], 
						      "title": "WeightLifting"
						    }, 
						    {
						      "creation_date": "Thu", 
						      "creator": "gwan", 
						      "mid": 9, 
						      "times": [
						        {
						          "date": "Wed", 
						          "time": "3am"
						        }, 
						        {
						          "date": "Tue", 
						          "time": "5am"
						        }
						      ]
						    }
						  ], 
						  "my_responded": [
						    {
						      "creation_date": "Thu", 
						      "creator": "hsolis", 
						      "finaltime": [], 
						      "mid": 2, 
						      "mine": True, 
						      "times": [
						        {
						          "date": "Fri", 
						          "time": "12pm"
						        }
						      ], 
						      "title": "Back Massage"
						    }, 
						    {
						      "creation_date": "Thu", 
						      "creator": "kl9", 
						      "finaltime": [], 
						      "mid": 4, 
						      "mine": False, 
						      "times": [
						        {
						          "date": "Fri", 
						          "time": "12am"
						        }
						      ], 
						      "title": "Code@Night"
						    }, 
						    {
						      "creation_date": "Thu", 
						      "creator": "hsolis", 
						      "finaltime": [
						        {
						          "date": "Fri", 
						          "time": "12pm"
						        }
						      ], 
						      "mid": 1, 
						      "mine": True, 
						      "times": [
						        {
						          "date": "Thu", 
						          "time": "8pm"
						        }, 
						        {
						          "date": "Fri", 
						          "time": "12pm"
						        }
						      ], 
						      "title": "Colonial Lunch"
						    }
						  ]
						}
						)

	# old sample test data to connect to front end
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
	# 					        "ksha",
	# 					        "tear",
	# 					        "test",
	# 					        "someone"
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
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "1pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "1pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "1pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "1pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "1pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "11pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "11pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "11pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Fri", 
	# 					          "time": "11pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "12pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "11pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "11pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "11pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "11pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "2pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "2pm"
	# 					        }, 
	# 					        {
	# 					          "day": "Thu", 
	# 					          "time": "2pm"
	# 					        }

	# 					      ], 
	# 					      "title": "Colonial Lunch"
	# 					    }
	# 					  ], 
	# 					  "my_requests": [
	# 					    {
	# 					      "creator": "gwan",
	# 					      "mid": 3, 
	# 					      "title": "Charter Friday",
	# 					      "times": [
	# 					          {
	# 					            "day": "Fri", 
	# 					            "time": "11pm"
	# 					          }, 
	# 					          {
	# 					            "day": "Fri", 
	# 					            "time": "1am"
	# 					          }
	# 					      ]
	# 					    }, 
	# 					    {
	# 					      "creator": "kl9", 
	# 					      "mid": 4,
	# 					      "title": "Code@Night",
	# 					      "times": [
	# 					          {
	# 					            "day": "Fri", 
	# 					            "time": "8pm"
	# 					          }
	# 					      ]
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
							init_data=init_data)

@app.route('/landing')
def landing():
	return render_template('landing.html')