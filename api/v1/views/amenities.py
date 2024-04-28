#!/usr/bin/python3
"""Amenities resources"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """Method that fetch all Amenities resources."""
    arr_am = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(arr_am)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Method that fetch Amenity resources by id."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Method that delete Amenity by id."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """Method that create Amenity record."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "name" not in request.json:
        abort(400, description="Missing Name")
    req = request.get_json()
    amenity = Amenity(name=req["name"])

    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """Method that update Amenity record by id."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "name" not in request.json:
        abort(400, description="Missing Name")
    req = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    for k in amenity.to_dict():
        for rk in req:
            if k == rk:
                amenity.__setattr__(str(rk), req[rk])
                break
    storage.save()
    return jsonify(amenity.to_dict()), 201
