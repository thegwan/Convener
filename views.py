# views.py

from flask import redirect, url_for, request, render_template
from flask_cas import CAS, login_required
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
	json = request.json
	print(json)
	return render_template('index.html', user=cas.username, token=cas.token, table=table)

@app.route('/landing')
def landing():
	return render_template('landing.html')