from quart import Blueprint

from .trips import trips_endpoints
from .trucks import trucks_endpoint
from .company import company_endpoint
from .register import register_endpoint
from .auth import web_endpoints

api_endpoints = Blueprint('api_endpoints', __name__)

api_endpoints.register_blueprint(trips_endpoints, url_prefix='/trip')
api_endpoints.register_blueprint(trucks_endpoint, url_prefix='/trucks')
api_endpoints.register_blueprint(company_endpoint, url_prefix='/companies')

api_endpoints.register_blueprint(web_endpoints, url_prefix='/web')
