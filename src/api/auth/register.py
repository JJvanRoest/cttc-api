from quart import Blueprint, request, jsonify

register_endpoint = Blueprint('register_endpoint', __name__)

@register_endpoint.route('/', methods=['POST'])
async def register():
    return jsonify({'message': 'Hello World'})