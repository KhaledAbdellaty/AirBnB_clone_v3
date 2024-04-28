#!/usr/bin/python3
"""Places reviews resources"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews')
def get_all_reviews(place_id):
    """Method that fetch all Reviews resources."""
    arr_reviews = [review.to_dict() for review in
                   storage.all(Review).values() if place_id == review.place_id]
    if len(arr_reviews) == 0:
        abort(404)
    return jsonify(arr_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Method that fetch Review resources by id."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Method that delete Review by id."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """Method that create Review record."""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif "text" not in request.json:
        abort(400, description="Missing text")
    elif "user_id" not in request.json:
        abort(400, description="Missing user_id")

    req = request.get_json()
    place = storage.get(Place, place_id)
    user = storage.get(User, req['user_id'])
    if place is None or user is None:
        abort(404)
    review = Review(text=req["text"],
                    place_id=place_id, user_id=req['user_id'])
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """Method that update Review record by id."""
    if not request.is_json:
        abort(400, description="Not a JSON")

    req = request.get_json()
    review = storage.get(Place, review_id)
    if review is None:
        abort(404)

    for k in review.to_dict():
        for rk in req:
            if k == rk:
                review.__setattr__(str(rk), req[rk])
                break
    storage.save()
    return jsonify(review.to_dict()), 201
