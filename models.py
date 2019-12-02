import datetime # S2 create the classes
from peewee import *
# S2 import * means import everything from Peewee, so that would be
# SqliteDatabase, and Model
from flask_login import UserMixin

# peewee is our form, it's like mongoose

DATABASE = SqliteDatabase('ucommute.sqlite') # you want to give it the name .sqlite extension
# when we want to go to production we'll use our postgres

# to be have correctly in flask-login's session/login in functionality, the User class
# must have some methods etc that Model doesn't have
# we could write them ourselves or we could additionally inherit from UserMixin which 
# will provide/implement them for us. See: https://flask-login.readthedocs.io/en/latest/
class User(UserMixin, Model):
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField()

	class Meta:
		database = DATABASE