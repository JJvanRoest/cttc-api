from quart import Blueprint

from .orders import orders_endpoint
from .trucks import trucks_endpoint

api_endpoints = Blueprint('api_endpoints', __name__)

api_endpoints.register_blueprint(orders_endpoint, url_prefix='/orders')
api_endpoints.register_blueprint(trucks_endpoint, url_prefix='/trucks')