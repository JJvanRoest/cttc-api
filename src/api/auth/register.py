from quart import Blueprint, request, jsonify

from src.database.user import User

register_endpoint = Blueprint('register_endpoint', __name__)

@register_endpoint.route('/', methods=['POST'])
async def register():
    
    return jsonify({'message': 'Hello World'})


@register_endpoint.route('/password_forgot', methods=['POST'])
async def password_forgot():
    
        return jsonify({'message': 'Hello World'})