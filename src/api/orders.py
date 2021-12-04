from quart import Blueprint, request, jsonify

orders_endpoint = Blueprint('orders_endpoint', __name__)

@orders_endpoint.route('/', methods=['GET'])
async def get_orders():
    return jsonify({'orders': []}), 200