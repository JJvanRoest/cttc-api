from quart import Blueprint

from .trips import trips_endpoints
from .trucks import trucks_endpoint
from .company import company_endpoint
from .auth import auth_endpoints

api_endpoints = Blueprint('api_endpoints', __name__)

api_endpoints.register_blueprint(trips_endpoints, url_prefix='/trip')
api_endpoints.register_blueprint(trucks_endpoint, url_prefix='/trucks')
api_endpoints.register_blueprint(auth_endpoints, url_prefix='/auth')
api_endpoints.register_blueprint(company_endpoint, url_prefix='/companies')
