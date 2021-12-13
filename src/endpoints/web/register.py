from quart import Blueprint, request, jsonify
from dataclasses import dataclass
from quart_schema import validate_request

from src.database.users import Users
from src.database.company_details import CompanyDetails

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
    password = req.get('password')
    email = req.get('email')
    company = req.get('company')
    company_det = CompanyDetails.get_or_none(company)
    if not company_det:
        return jsonify({'message': 'Company not found'}), 404
    user = Users.create(username=username, password=password,
                        email=email, company=company_det)
    return jsonify({'message': user})


@register_endpoint.route('/password_forgot', methods=['POST'])
async def password_forgot():

    return jsonify({'message': 'Hello World'})
