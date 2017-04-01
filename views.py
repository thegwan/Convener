# views.py

from main import app

# connect the index webpage
@app.route('/')
def index():
	return 'This is the homepage'