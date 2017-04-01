# main.py

from flask import Flask

app = Flask(__name__)
from views import *

# only start the web server when this file is called directly
if __name__ == "__main__":
	app.run(debug = True)