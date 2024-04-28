#!/usr/bin/python3
"""States resources"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """Method that fetch all States resources."""
    arr_states = [state.to_dict() for
                  state in storage.all('State').values()]
    return jsonify(arr_states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Method that fetch State resources by id."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/', methods=['POST'])
def post_state():
    """Method that delete State by id."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "name" not in request.json:
        abort(400, description="Missing Name")

    req = request.get_json()
    state = State(**req)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """Method that create State record."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "name" not in request.json:
        abort(400, description="Missing Name")

    req = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    for k in state.to_dict():
        for rk in req:
            if rk not in ['id', 'created_at', 'updated_at']:
                state.__setattr__(str(rk), req[rk])
                break
    storage.save()
    return jsonify(state.to_dict()), 200
