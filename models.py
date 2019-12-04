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

	class Meta: #special constructor that will give our class instructions telling our
	# model to connect to a specific database
		database = DATABASE


class Trip(Model):
	user_id = IntegerField()
	color_id = IntegerField()
	origin = CharField()
	destination = CharField()
	direction = CharField()
	transfer = BooleanField()

	class Meta:
		database = DATABASE

class Station(Model):
	user_id = CharField()
	stop_id = CharField() # Blue Line O-Hare Station = BL-A
	station_name = CharField()
	line_color = CharField()
	direction = CharField()
	transfer = BooleanField()
	# order_number = Str() not necessary because station name is a more symantic name for a key
	class Meta:
		database = DATABASE


def initialize(): # i'm making this name up
	DATABASE.connect()
	DATABASE.create_tables([User, Trip, Station], safe=True) #safe=True checks to see if the table was created
	# if it was, don't erase it
	print("TABLES created")
	DATABASE.close()


