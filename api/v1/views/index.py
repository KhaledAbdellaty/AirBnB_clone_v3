#!/usr/bin/python3
"""Defines a status route for the HolbertonBnB API."""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status_route():
    """Returns the server status.

    Returns:
        JSON object with the current server status.
    """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def get_stats():
    """Retrives the count of each object type.

    Returns:
        JSON object with the number of objects by type."""
    classes = {
           "amenities":"Amenity", "cities":"City",
          "places" :"Place", "reviews":"Review", "states":"State", "users":"User",
    }

    dic = {}
    for key in classes:
        dic[key] = storage.count(classes[key])
    return dic
