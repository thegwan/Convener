# views.py

from flask import request, render_template
from main import app

# connect the index webpage
@app.route("/", methods=['GET', 'POST'])
def index():
	#return "This is the homepage. Method used: %s" % request.method
	return render_template("calendar.html")