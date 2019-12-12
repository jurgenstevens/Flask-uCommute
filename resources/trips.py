import models
from peewee import *
from flask import Blueprint, jsonify, request # import the request object
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict
# from resources.users import users
# from resources.stations import station


# first argument is blueprints name
# second argument is its import name
# The third argument is the url_prefix so we dont have to prefix all our
# apis with /api/v1 url_prefix app.use(/trips)
trip = Blueprint('trips', 'trip')


# INDEX ROUTE
@trip.route('/', methods=["GET"])
@login_required
def trip_index():
	try:
		this_user_trip_instances = models.Trip.select().where(models.Trip.user_id == current_user.id)
		# print('THESE ARE THE TRIP INSTANCES')
		# print(this_user_trip_instances)
		this_user_trip_dicts = [model_to_dict(trip) for trip in this_user_trip_instances]
		# print('THESE ARE THE TRIP DICTS')
		# print(this_user_trip_dicts)

		return jsonify(data=this_user_trip_dicts, status={"code": 200, "message": "Here are your trips!"})
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'ERROR'}), 401

# crete a trip
@trip.route('/<origin>/<destination>', methods=["POST"])
# user must be logged in
@login_required
def create_a_trip(origin, destination):
	# try:
		payload = request.get_json()
		# print(payload)
		# # picking a start point
		trip_start = models.Station.get_by_id(origin)
		# # trip_start = models.Station.create(**payload)
		# # pick destination
		trip_end = models.Station.get_by_id(destination)

		trip_start_dict = model_to_dict(trip_start)
		trip_end_dict = model_to_dict(trip_end)

		# print("THIS IS THE START vvvvvvv");
		# print(trip_start_dict);
		# print(type(payload['transfer']))

		trip = models.Trip.create(
			user_id=current_user.id,
			trip_name="My Trip",
			color_id="Orange",
			origin=trip_start.id, 
			destination=trip_end.id, 
			direction="Inbound",
			transfer=False
			)
			# grab all of the middle stops in between to show to user
		# print(type(trip))
		# trips = model_to_dict(trip)
		# print("we created trip successfully")
		# trip_dict = model_to_dict(trip)
		print(model_to_dict(trip))
		return jsonify(data={
			
			'start': model_to_dict(trip_start), 
			'end': model_to_dict(trip_end)}, 
			status={'code': 200, 'message': 'Your trip has been successfully created!'}) 
			#for debugging only
		# return jsonify(data=model_to_dict(trip), status={"code": 201, "message": "Trip has been successfully created."}), 201
			# 'trip': model_to_dict(trip)
	# except models.DoesNotExist:
	# 	print("error")
		return jsonify(data={}, status={'code': 400, 'message': 'ERROR'}), 400
# station_id = ''
# if( this station is part of the Pink line):
	# station_id += "P"
# if (this station is # 25 on the routes ):
	# station_id += "25"

# JSON TO CREATE A TRIP:
# {
# 	"user_id": "1",
#	"trip_name": "Work Commute"
# 	"color_id": "Orange",
# 	"origin": "O-A",
# 	"destination": "O-G",
# 	"direction": "N",
# 	"transfer": "false"
# }

# save a trip

# this is the SHOW route to see specific trips
@trip.route('/<id>', methods=["GET"])
@login_required
def pick_your_trip(id):
	trip = models.Trip.get_by_id(id)

	return jsonify(data=model_to_dict(trip), status={"code": 200, "message": "Here's the trip you chose!"}), 200


# query = models.Trips.select().where()

# this is the UPDATE route
@trip.route('/<id>', methods=["PUT"])
@login_required
def update_trip(id):
	try:
		payload = request.get_json()

		query = models.Trip.update(**payload).where(models.Trip.id==id)
		query.execute()

		trip = models.Trip.get_by_id(id)
		trip_dict = model_to_dict(trip)

		return jsonify(data=trip_dict, status={"code": 200, "message": "Your trip has been updated successfully!"})
	except models.DoesNotExist:
		jsonify(data={}, status={"code": 401, "message": "Error deleting trip."})

# and last but not least, this is the DELETE route
@trip.route('/<id>', methods=["DELETE"])
@login_required
def delete_trip(id):
	query = models.Trip.delete().where(models.Trip.id == id)
	query.execute()
	return jsonify(data='The trip has been successfully deleted', status={"code": 200, "message": "Trip deleted successfully"})







