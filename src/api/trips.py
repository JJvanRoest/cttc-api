from quart import Blueprint, request, jsonify

trips_endpoints = Blueprint('trips_endpoints', __name__)


@trips_endpoints.route('/', methods=['GET'])
async def get_trip():
    return jsonify({'trip': []}), 200
