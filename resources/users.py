import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

#make this a blueprint
users = Blueprint('users', 'users')

# @users.route('/', methods=['GET'])
# def test_user_controller():
#   return "hi you have a user resource"

@users.route('/register', methods=['POST'])
def register():
	# this is like grabbing req.body in a var
	payload = request.get_json()
	# emails are case insensitive in the world
	payload['email'].lower()

	try:
		models.User.get(models.User.email == payload['email'])

		#if we didn't throw an error, the user must already exist
		return jsonify(data={}, status={'code': 401, 'message': 'A user with that email already exists'}), 401

	except models.DoesNotExist:
		#if the user wasn't there, this "error" would happen, which means
		# we're safe to go ahead and register them

		#encrypt password with bcrypt
		# note: we are replacing password in the payload dict with the hashed password
		payload['password'] = generate_password_hash(payload['password'])

		#register them in the db # note the ** is like the spread operator in JS (...)
		#shorthand for writing out all the properties like we did in dog create
		user = models.User.create(**payload)

		# this is where we actually use flask-login
		# this "logs in" the user and starts a session
		login_user(user)

		user_dict = model_to_dict(user)

		# check out the user we just created
		print(user_dict)

		# we're gonna send this back to client, we don't need the password, so why risk it?
		del user_dict['password']

		return jsonify(data=user_dict, status={'code': 201, 'message': 'Successfully registerd {}'.format(user_dict['email'])}), 201

@users.route('/login', methods=['POST'])
def login():
	payload = request.get_json()

	try:
		#look up user by email
		user = models.User.get(models.User.email == payload['email'])
		# so we can access the info in user
		user_dict = model_to_dict(user)
		# check user's password using bcrypt
		if(check_password_hash(user_dict['password'], payload['password'])):
			# everything is good

			# this is how you log the user in the app using flask_login
			login_user(user)
			del user_dict['password']

			return jsonify(data=user_dict, status={'code': 200, 'message': 'Successfully logged in {}'.format(user_dict['email'])}), 200

		else:
			print('This password doesnt work')
			return jsonify(data={}, status={'code': 401, 'message': 'Email or password are incorrect'}), 401


	except models.DoesNotExist:
		print('Email not found')
		return jsonify(data={}, status={'code': 401, 'message': 'Email or password are incorrect'}), 401

# {
# 	"username": "jurgen",
# 	"email": "jurgen@email.com",
# 	"password": "1234"
# }



@users.route('/logged_in', methods=['GET'])
def get_logged_in_user():
	# manually write logic in a route based on whether a user is logged in or not
	if not current_user.is_authenticated:
		return jsonify(data={}, status={
			'code': 401,
			'message': "No user is currently logged in"
			}), 401
	else:
		#print(current_user) # inspect just what current user's ID
		# print(type(current_user)) # what is a werkzeug bro??
		user_dict = model_to_dict(current_user)
		print(user_dict)
		user_dict.pop('password')
		return jsonify(data=user_dict, status={'code': 200, 'message': "Current user is {}".format(user_dict['email'])}), 200


# we'll make a logout route below
@users.route('/logout', methods=['GET'])
def logout():
	email = model_to_dict(current_user)['email']
	logout_user()
	return jsonify(data={}, status={'code': 200, 'message': "You've successfully logged out {}".format(email)}), 200
















