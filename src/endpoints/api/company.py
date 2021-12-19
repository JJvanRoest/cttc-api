from enum import Enum
from playhouse.shortcuts import dict_to_model, model_to_dict
from quart import jsonify, request
from quart.blueprints import Blueprint
import quart_schema as qs
from dataclasses import dataclass

from config import CONFIG
from ...database.company import Company
from ...database.database import database

from peewee import IntegrityError, InternalError


from typing import Dict, Optional, List, Tuple
from pydantic.types import Json

from ..helpers.auth import hash_api_key, verify_api_key, get_random_string
from ..helpers.validation import validate_request


company_endpoint = Blueprint('company', __name__)


class CompanyTypes(Enum):
    """
    Enum for company types
    """
    TRUCK_COMPANY = 'TC'
    DISTRIBUTION_CENTER = 'DC'


@dataclass
class CompanyRegisterSchema:
    company_name: str
    company_location: str
    company_type: CompanyTypes
    company_api_url: str


@company_endpoint.route('/', methods=['GET', 'POST'])
async def companies():
    if request.method == "POST":
        req = await request.get_json()
        validate_request(model=CompanyRegisterSchema, source=req)
        return create_company(req)
    elif request.method == "GET":
        return jsonify(get_companies()), 200


@company_endpoint.route('/<int:company_id>', methods=['GET'])
async def get_company(company_id: int):
    company_dict: Optional[Dict] = get_company_by_id(company_id)
    if company_dict is None:
        return jsonify({'message': 'Company not found'}), 404

    return jsonify(company_dict), 200


def get_company_by_id(company_id: int) -> Optional[Dict]:
    company: Optional[Company] = Company.get_or_none(Company.id == company_id)
    if not company:
        return None
    company: Dict = model_to_dict(company)
    company.pop("api_key")
    return company


def get_companies() -> List[Dict]:
    companies: List[Dict] = []
    company_details = Company.select()
    for company in company_details:
        company_dict = model_to_dict(company)
        company_dict.pop("api_key")
        companies.append(company_dict)
    return companies


def create_company(req: Json) -> Tuple:
    api_key_plain = get_random_string()
    hashed_api_key = hash_api_key(api_key_plain)
    with database.atomic():
        try:
            company = Company.create(
                company_name=req["company_name"],
                company_location=req["company_location"],
                company_type=req["company_type"],
                company_api_url=req["company_api_url"],
                api_key=hashed_api_key,
            )
        except (IntegrityError, InternalError):
            return jsonify({"error": "Duplicate entry."}), 422
    company_dict = model_to_dict(company)
    # Return the plain text api key upon registration, unless api keys have not been enabled.
    if CONFIG.auth['api_key_enabled']:
        company_dict["api_key"] = api_key_plain
    else:
        company_dict.pop("api_key")
    return jsonify(company_dict), 201
