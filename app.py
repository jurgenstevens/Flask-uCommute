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
login_manager.init_app()
# S2 carries on to models.py