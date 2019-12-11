import models
from flask import Blueprint, jsonify, request # import the request object
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict
# from nose.tools import assert_true # use the following two imports for 3rd party API requests
# import requests


station = Blueprint('stations', 'station')

# def test_request_response():
# 	# Sending a request to the API server and storing the response
# 	response = requests.get('https://data.cityofchicago.org/resource/8pix-ypme.json')
# 	# Confirm that the request-response cycle completed successfully
# 	assert_true(response.ok)

# S4 what will be attached VVV routes and CRUD routes and RESTful routes
# this is the index route
@station.route('/', methods=["GET"])
@login_required ## this will make this unavailable to users who aren't logged in # use authentication required instead create a conditional in react that will only allow user 1 being you to alter station info
def stations_index():
	# S5 find the stations and change each one to a dictionary into a new array
	try:
		this_user_station_instances = models.Station.select().where(models.Station.user_id == current_user.id)
		this_user_station_dicts = [model_to_dict(station) for station in this_user_station_instances]

		return jsonify(data=this_user_station_dicts, status={"code": 200, "message": "Success!"})
	except models.DoesNotExist:
		return jsonify(data={}, status={"code": 401, "message": "Error getting the sources."})

# S5 add the POST where you can insert JSON
# CREATE ROUTE
@station.route('/', methods=["POST"])
def create_station():
	payload = request.get_json()

	station = models.Station.create(user_id=payload['user_id'], stop_id=payload['stop_id'], station_name=payload['station_name'], line_color=payload['line_color'], direction=payload['direction'], transfer=payload['transfer'])
	# print(dir(station))

	# see the methods
	station_dict = model_to_dict(station)

	return jsonify(data=station_dict, status={"code": 201, "message": "Success"}), 201

# CREATE A STATION JSON TEMPLATE FOR POSTMAN
# {
#	"user_id": "1",
# 	"stop_id": "O-A",
# 	"station_name": "Midway",
# 	"line_color": "Orange",
# 	"direction": "N",
# 	"transfer": "false"
# }

# S9 Create a route that loops through stations
@station.route('/<line_color>/<direction>', methods=["GET"])
def find_by_line(line_color, direction):

	line_stations = models.Station.select().where(
		models.Station.line_color == line_color, models.Station.direction == direction
	)
	# .first() display just one but DoesNotExist
	# must loop through list to change them to dicts in order to display bc model_to_dict only does one, not multiple
	line_stations_dict = [model_to_dict(station) for station in line_stations]

	

	return jsonify(data=line_stations_dict, status={"code": 200, "message": "Here are your stations"})



#S6 create the SHOW route
@station.route('/<id>', methods=["GET"])
def find_a_station(id):
	print(id)
	station = models.Station.get_by_id(id)

	return jsonify(data=model_to_dict(station), status={"code": 200, "message": "Success!"})

# S7 create the UPDATE route
@station.route('/<id>', methods=["PUT"])
def updated_station(id):
	payload = request.get_json()

	query = models.Station.update(**payload).where(models.Station.id == id)
	query.execute()

	station = models.Station.get_by_id(id)
	station_dict = model_to_dict(station)

	return jsonify(data=station_dict, status={"code": 200, "message": "Station has been edited!"})

#S8 create the DELETE route!
@station.route('/<id>', methods=["DELETE"])
def delete_station(id):
	query = models.Station.delete().where(models.Station.id == id)
	query.execute()
	return jsonify(data='Station successfully deleted', status={"code": 200, "message": "Station has been successfully deleted."})























