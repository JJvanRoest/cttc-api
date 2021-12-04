from quart import Blueprint, request, jsonify

trucks_endpoint = Blueprint('trucks_endpoint', __name__)

@trucks_endpoint.route('/', methods=['GET'])
async def get_trucks():
    return jsonify({'trucks': []}), 200