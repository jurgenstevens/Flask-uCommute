import os
import datetime # S2 create the classes
from peewee import *
# S2 import * means import everything from Peewee, so that would be
# SqliteDatabase, and Model
from playhouse.db_url import connect
from flask_login import UserMixin

# peewee is our form, it's like mongoose
if 'ON_HEROKU' in os.environ: 
	DATABASE = connect(os.environ.get('DATABASE_URL')) 
# later we will manually add this env var                           
# in heroku so we can write this code
# heroku will add this 
# env var for you 
# when you provision the
# Heroku Postgres Add-on
else:
	DATABASE = SqliteDatabase('ucommute.sqlite') 
  # OPTIONALLY: instead of the above line, here's how you could have your 
  # local app use PSQL instead of SQLite:

  # DATABASE = PostgresqlDatabase('dog_demo', user='reuben')  

  # the first argument is the database name -- YOU MUST MANUALLY CREATE 
  # IT IN YOUR psql TERMINAL
  # the second argument is your Unix/Linux username on your computer

# you want to give it the name .sqlite extension
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

class Station(Model):
	user_id = ForeignKeyField(User, backref="users")
	stop_id_origin = CharField() # Blue Line O-Hare Station = BL-A
	stop_id_dest = CharField() 
	station_name = CharField()
	line_color = CharField()
	direction = CharField()
	transfer = BooleanField()
	# trips = CharField()
	# transfer_to = CharField() ##drop database and include what line_color user can transfer to
	class Meta:
		database = DATABASE

class Trip(Model):
	user_id = CharField()
	trip_name = CharField()
	color_id = CharField() # probably won't need this
	origin = ForeignKeyField(Station, backref="stations")
	destination = ForeignKeyField(Station, backref="stations")
	direction = CharField()
	transfer = BooleanField()
	# transfer_to = CharField()

	class Meta:
		database = DATABASE


# class Transfer(Model):
# 	user_id = CharField()
# 	color_id = CharField()


def initialize(): # i'm making this name up
	DATABASE.connect()
	DATABASE.create_tables([User, Trip, Station], safe=True) #safe=True checks to see if the table was created
	# if it was, don't erase it
	print("TABLES created")
	DATABASE.close()


