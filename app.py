import os
# virtualenv .env -p python3
# source .env/bin/activate 
# pip install -r requirements.txt
# run "pip3 install -r requirements.txt." in git after cloning an assignment
# run source .env/bin/activate in git
# create a file called "ucommute.sqlite"

from flask import Flask, jsonify, g # g = global variable
from flask_cors import CORS
#this is the main tool for coordinating session/login stuff in our app
from flask_login import LoginManager
from resources.users import users
from resources.stations import station
from resources.trips import trip

import models #S1 we gotta import the object and method that's going to create our app

DEBUG = True #S1 this gives us pretty error message
PORT = 8000

#S1 Initialize an instance of the Flask class. This starts the website!
app = Flask(__name__)


# S1 we must set up a session secret to use flask-login
app.secret_key = "This is a super secret string that you'll never get outta me"

# S1 instantiate that class to get a login_manager
login_manager = LoginManager()

# S1 actually connect the app with login_manager
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

# so HTML pages that say 403 unauthorized are nice, but we want to send json instead
# so let's customize the 'unauthorized' behavior
# This is from the docs
@login_manager.unauthorized_handler
def unauthorize():
	return jsonify(data={
		'error': "User not logged in"
		}, status={
		'code': 401,
		'message': "You must be logged in to access that source"
		}), 401

#S5
# localhost:3000 will be the react app when it's created
# localhost:3000 represents a client that will communicate with our API
# supports_credentials allows cookies to be sent to our API session
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(station, origins=['http://localhost:3000'], supports_credentials=True) # add this line later
CORS(trip, origins=['http://localhost:3000'], supports_credentials=True) # add this line later



#S6 - this sets up our routes on our app - app.use(/dsf, tripController
app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(station, url_prefix='/api/v1/stations')
app.register_blueprint(trip, url_prefix='/api/v1/trips') 

@app.before_request #this is a decorator function, runs before another function, so we will run the flask before_request before our before_request
def before_request():
	""" Connect to the database before each request. """
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	""" Close the database connection after each request. """
	g.db.close()
	return response # give response back to client, in this case, some JSON

# Here's a route in flask
# Note: the default URL ends in / 
# @app.route('/')
# def index():
# 	return 'Hello, world!'

# it's finicky about types -- you can't return just a string
# @app.route('/test')
# def trip():
# 	return ['a', 'trip'] # note -- you can't return array

@app.route('/test_json')
def train_json():
	return jsonify(['orange', 'line']) # but you can return it as json
										# note we added an import for this function
# jsonify can take key value pairs
@app.route('/trip_json')
def trip_json():
	return jsonify(line="orange", stop="halsted")

#how to make it take url paramater
@app.route('/say_hello/<username>') # when someone goes here...
def hello(username): # DO this.
	return "Hello {}".format(username)

# ADD THESE THREE LINES -- because in production the app will be run with 
# gunicorn instead of by the three lines below, so we want to initialize the
# tables in that case as well
if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()
  
# Run the app when the program starts
if __name__ == '__main__':
	models.initialize() #invokes the function that creates our tables models.py
	app.run(debug=DEBUG, port=PORT)


# S2 carries on to models.py!