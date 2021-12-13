from playhouse.shortcuts import dict_to_model, model_to_dict
from quart import jsonify, request
from quart.blueprints import Blueprint
from quart_schema import validate_request
from dataclasses import dataclass
from ..database.company_details import CompanyDetails

company_endpoint = Blueprint('companies', __name__)


@company_endpoint.route('/', methods=['GET'])
async def get_companies():
    company_details = CompanyDetails.select()
    companies: list[CompanyDetails] = []
    for company in company_details:
        companies.append(model_to_dict(company))
    json_res = jsonify(companies)
    return json_res, 200


@company_endpoint.route('/<int:company_id>', methods=['GET'])
async def get_company(company_id: int):
    company_details = CompanyDetails.get_or_none(
        CompanyDetails.id == company_id)
    if company_details is None:
        return jsonify({'message': 'Company not found'}), 404
    company = model_to_dict(company_details)
    return jsonify(company), 200


@dataclass
class CompanyDetailsSchema:
    name: str
    location: str


@company_endpoint.route('/register', methods=['POST'])
@validate_request(CompanyDetailsSchema)
async def register_company():
    req = await request.get_json()
    company_model = dict_to_model(CompanyDetails, req)
    company = CompanyDetails.create(company_model)
    return jsonify(company), 201
