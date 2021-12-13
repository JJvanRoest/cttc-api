from typing import Optional

from cryptography.fernet import Fernet
import jwt

from quart import request
from config import Config

def check_auth() -> bool:
    encoded_jwt = get_req_token()

    if not encoded_jwt:
        return False

    try:
        decoded_jwt = jwt.decode(encoded_jwt, Config.SECRET_KEY, algorithms=['HS256'])
    except (jwt.exceptions.DecodeError, jwt.InvalidTokenError, jwt.exceptions.ExpiredSignatureError):
        return False
    return False

def get_req_token() -> str:
    """
    Get the token from the request headers or query params.
    :return: request jwt token.
    """
    try:
        return request.headers.get('Authorization').split(' ')[1]   # Authorization: Bearer <token>
    except IndexError:
        pass
    return request.args.get('token')

def encode_auth_token(req) -> Optional[str]:
    """
    Generates authentication bearer token
    """
    try:
        req_json = req.get_json()
        email, password = None

        if req_json is not None:
            email = req_json.get('email')
            password = req_json.get('password')
        
        if email is None and password is None:
            auth_token = get_req_token()
        
        if auth_token is not None:
            try:
                jwt.decode()
            except:
                pass