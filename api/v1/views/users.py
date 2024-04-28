#!/usr/bin/python3
"""Users resources"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """Method that fetch all Users resources."""
    arr_users = [user.to_dict() for
                 user in storage.all(User).values()]
    return jsonify(arr_users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Method that fetch User resources by id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Method that delete User by id."""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def post_user():
    """Method that create User record."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "email" not in request.json:
        abort(400, description="Missing email")
    elif "password" not in request.json:
        abort(400, description="Missing password")

    req = request.get_json()
    user = User(**req)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """Method that update User record by id."""
    if not request.is_json:
        abort(400, description="Not a JSON")

    req = request.get_json()
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    for key in req:
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            user.__setattr__(str(key), req[key])

    storage.save()
    return jsonify(user.to_dict()), 200
