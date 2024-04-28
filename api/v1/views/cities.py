#!/usr/bin/python3
"""Cities resources"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    """Method that fetch all cities resources."""
    arr_cities = [city.to_dict() for city in storage.all(City).values()
                  if state_id == city.state_id]
    if len(arr_cities) == 0:
        abort(404)
    return jsonify(arr_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Method that fetch city resources by id."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Method that delete City by id."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """Method that create City record."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "name" not in request.json:
        abort(400, description="Missing Name")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req = request.get_json()
    city = City(state_id=state_id, name=req["name"])

    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """Method that update City record by id."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "name" not in request.json:
        abort(400, description="Missing Name")

    req = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    for k in req:
        if k not in ["id", "created_at", "updated_at"]:
            city.__setattr__(str(k), req[k])

    storage.save()
    return jsonify(city.to_dict()), 200
