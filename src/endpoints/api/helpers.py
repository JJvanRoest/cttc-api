from typing import Optional

from quart import request
from cryptography.fernet import Fernet
import jwt
from ..helpers.auth import check_auth


def require_auth(type: int = 0):
    """
    Decorator for requiring authentication for a request.
    :param type: 0 = normal auth, 1 = TruckCompany, 2 = DistributionCenter 
    """
    def wrapper(f):
        def wrapped_f(*args, **kwargs):
            authenticated = check_auth(type)
            if not authenticated:
                return {'error': 'You must be logged in to access this resource.'}, 401
            return f(*args, **kwargs)
        return wrapped_f
    return wrapper
