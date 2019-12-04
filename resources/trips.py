import models
import xmltodict
from flask import Blueprint, jsonify, request # import the request object
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is its import name
# The third argument is the url_prefix so we dont have to prefix all our
# apis with /api/v1 url_prefix app.use(/trips)
trip = Blueprint('trips', 'trip')




# query = models.Trips.select().where()

# station_id = ''
# if( this station is part of the Pink line):
	# station_id += "P"
# if (this station is # 25 on the routes ):
	# station_id += "25"

# create 
