#!/usr/bin/python3
"""Defines the view for places amenities Api calls"""
import os
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    """getting a list of amenities
    from a place on id.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity(place_id, amentiy_id):
    """remote an Amenity object from a place based on id."""
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_amenity(place_id, amenity_id):
    """Addes an Amenity object from a place based on id."""
    place = storage.get("Place", place_id)
    amentiy = storage.get("Amentiy", amenity_id)
    if place is None:
        abort(404)
    if amentiy is None:
        abort(404)
    if amentiy in place.amenities:
        return jsonify(amentiy.to_dict()) 200

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
