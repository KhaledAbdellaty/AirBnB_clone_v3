#!/usr/bin/python3
"""Entry point for HolbertonBnB API calls."""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def not_found(e):
    return jsonify({"error": e.description}), 400


if __name__ == "__main__":
    from os import getenv
    app_host = getenv('HBNB_API_HOST') or "0.0.0.0"
    app_port = int(getenv('HBNB_API_PORT') or "5000")
    app.run(host=app_host, port=app_port, threaded=True)
