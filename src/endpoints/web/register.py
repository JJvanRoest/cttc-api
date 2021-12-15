from quart import Blueprint, request, jsonify
from dataclasses import dataclass
from quart_schema import validate_request
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError
from passlib.hash import sha256_crypt


from src.database.users import Users
from src.database.company import Company
from src.database.database import database as db

register_endpoint = Blueprint('register_endpoint', __name__)


@dataclass
class RegisterRequest:
    username: str
    password: str
    email: str
    company: int


@register_endpoint.route('/', methods=['POST'])
@validate_request(RegisterRequest)
async def register(data: RegisterRequest):
    req = await request.get_json()
    username = req.get('username')
    password_plain = req.get('password')
    password = hash_password(password_plain)
    email = req.get('email')
    company = req.get('company')
    with db.atomic():
        company_det = Company.get_or_none(company)
    if not company_det:
        return jsonify({'message': 'Company not found'}), 404

    with db.atomic():
        user = Users.create(username=username, password=password,
                            email=email, company=company_det)
    user_dict = model_to_dict(user)
    user_dict.pop('password')
    user_dict.pop('password_reset_token')
    user_dict['company'].pop("api_key")
    return jsonify({'message': user_dict})


@register_endpoint.route('/password_forgot', methods=['POST'])
async def password_forgot():
    return jsonify({'message': 'This method is not implemented yet'})


def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)
