from quart import Blueprint, request, jsonify

login_endpoint = Blueprint('login_endpoint', __name__)

@login_endpoint.route('/', methods=['POST'])
async def login():
    return jsonify({'message': 'Hello World!'})