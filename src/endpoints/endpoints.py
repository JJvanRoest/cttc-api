from quart import Blueprint

from .api.api import api_endpoints
from .web.web import web_endpoints

endpoints = Blueprint('endpoints', __name__)

endpoints.register_blueprint(web_endpoints, url_prefix='/web')
endpoints.register_blueprint(api_endpoints, url_prefix='')
