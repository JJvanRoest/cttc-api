from quart import Blueprint, request, jsonify

from .login import login_endpoint
from .register import register_endpoint

auth_endpoints = Blueprint('auth_endpoints', __name__)

auth_endpoints.register_blueprint(login_endpoint, url_prefix='/login')
auth_endpoints.register_blueprint(register_endpoint, url_prefix='/register')



