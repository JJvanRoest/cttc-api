from passlib.hash import sha256_crypt
from quart import Blueprint, request, jsonify
from dataclasses import dataclass
from quart_schema import validate_request
from playhouse.shortcuts import model_to_dict
from ...endpoints.helpers.auth import create_jwt_token
from typing import Dict, Optional, List, Tuple
from src.database.users import Users
from src.database.database import database as db

login_endpoint = Blueprint('login_endpoint', __name__)


@dataclass
class LoginRequestSchema:
    email: str
    password: str


@login_endpoint.route('/', methods=['POST'])
@validate_request(LoginRequestSchema)
async def login(data: LoginRequestSchema):
    req = await request.get_json()
    email = req.get('email', None)
    plain_password = req.get('password', None)

    error_message = jsonify(
        {'message': 'Password or email incorrect.', "success": False}), 401

    if not email or not plain_password:
        return error_message

    with db.atomic():
        user = Users.get_or_none(Users.email == email)

    if not user:
        return error_message

    if not user.active:
        return jsonify(
            {'message': 'Account is not active.', "success": False}), 401

    verified = verify_password(user, plain_password)
    if not verified:
        return error_message

    user_dict = get_clean_user(user)
    user_token = await create_access_token(user_dict)
    token = f"Bearer {user_token}"
    return jsonify({'message': user_dict, "token": token, 'success': True})


async def create_access_token(user: Dict) -> str:
    return await create_jwt_token(user)


def verify_password(user: Users, plain_pass: str) -> bool:
    return sha256_crypt.verify(plain_pass, user.password)


def get_clean_user(user: Users) -> Dict:
    user_dict = model_to_dict(user)
    user_dict.pop('password')
    user_dict.pop('password_reset_token')
    user_dict['company'].pop('api_key')
    return user_dict
