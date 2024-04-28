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
    classes = [
           "Amenity", "City",
           "Place", "Review", "State", "User",
    ]

    dic = {}
    for cls_name in classes:
        key = cls_name

        dic[key.lower()] = storage.count(key)

    return dic
