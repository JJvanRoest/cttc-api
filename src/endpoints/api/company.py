from enum import Enum
from playhouse.shortcuts import dict_to_model, model_to_dict
from quart import jsonify, request
from quart.blueprints import Blueprint
import quart_schema as qs
from dataclasses import dataclass
from ...database.company import Company
from ...database.database import database

from peewee import IntegrityError, InternalError
# TODO move to helpers
from pydantic.dataclasses import dataclass as pydantic_dataclass, is_builtin_dataclass
from pydantic import ValidationError
from pydantic.types import Json

from werkzeug.exceptions import BadRequest

from typing import Dict, Optional, Union, List

from passlib.hash import sha256_crypt

import random
import string

company_endpoint = Blueprint('company', __name__)


class RequestSchemaValidationError(BadRequest):
    def __init__(self, validation_error: Union[TypeError, ValidationError]) -> None:
        super().__init__()
        self.validation_error = validation_error


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
async def get_companies():
    if request.method == "POST":
        validate_request(model=CompanyRegisterSchema, source=(await request.get_json()))
        print(request)
        req = await request.get_json()
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
            except (IntegrityError, InternalError) as error:
                return jsonify({"error": "Duplicate entry."}), 422
        company_dict = model_to_dict(company)
        # Return the plain text api key upon registration
        company_dict["api_key"] = api_key_plain
        return jsonify(company_dict), 201
    elif request.method == "GET":
        return jsonify(get_companies()), 200


@company_endpoint.route('/<int:company_id>', methods=['GET'])
async def get_company(company_id: int):
    company_dict: Optional[Dict] = get_company_by_id(company_id)
    if company_dict is None:
        return jsonify({'message': 'Company not found'}), 404

    return jsonify(company_dict), 200


def validate_request(model, source: Json) -> bool:
    model_class = pydantic_dataclass(model)
    try:
        model = model_class(**source)
    except (TypeError, ValidationError) as error:
        raise RequestSchemaValidationError(error)
    return True


def get_random_string() -> str:
    chars = string.ascii_letters + string.punctuation
    size = 12
    return ''.join(random.choice(chars) for _ in range(size))


def hash_api_key(api_key: str) -> str:
    return sha256_crypt.hash(api_key)


def verify_api_key(company: Company, api_key: str) -> bool:
    return sha256_crypt.verify(api_key, company.api_key)


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
