#!/usr/bin/python3
"""Places resources"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_all_places(city_id):
    """Method that fetch all Places resources."""
    arr_places = [places.to_dict() for places in storage.all(Place).values()
                  if city_id == places.city_id]
    if len(arr_places) == 0:
        abort(404)
    return jsonify(arr_places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Method that fetch Place resources by id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Method that delete Plcae by id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """Method that create new Place record."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "name" not in request.json:
        abort(400, description="Missing Name")
    elif "user_id" not in request.json:
        abort(400, description="Missing user_id")

    req = request.get_json()
    city = storage.get(City, city_id)
    user = storage.get(User, req['user_id'])
    if city is None or user is None:
        abort(404)
    place = Place(name=req["name"], city_id=city_id, user_id=req['user_id'])
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """Method that update Place record by id."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    req = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    for key in req:
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            place.__setattr__(str(key), req[key])
        storage.save()
    return jsonify(place.to_dict()), 201
