from uuid import uuid4, UUID
from enum import Enum
from typing import List, Dict, Tuple
from dataclasses import dataclass
from pydantic.types import Json
from quart import Blueprint, request, jsonify

from endpoints.helpers.validation import validate_request

trips_endpoints = Blueprint('trips_endpoints', __name__)


class CargoTypes(Enum):
    """
    Enum for cargo types
    """
    ALCOHOL = 'Alcohol'
    BEER = 'Beer'
    WINE = 'Wine'
    TOBACCO = 'Tobacco'
    PETROL = 'Petrol'
    DIESEL = 'Diesel'
    OIL = 'Oil'
    LPG = 'LPG'
    JUICE = 'Juice'
    VEGETABLE_JUICE = 'Vegetable Juice'
    FRUIT_JUICE = 'Fruit Juice'
    MINERAL_WATER = 'Mineral Water'
    UNTAXED = 'Untaxed'


@dataclass
class TripRequestSchema:
    id: UUID
    start_location: str
    pickup_location: str
    destination_location: str
    payload: List[Dict[CargoTypes, int]]
    truck_license_plate: str
    truck_location: str
    current_truck_load: int


@trips_endpoints.route('/', methods=['GET', 'POST'])
async def trips():
    if request.method == "POST":
        req = await request.get_json()
        print(req)
        validate_request(model=TripRequestSchema, source=req)
        return create_trip(req)
    else:
        return get_trips()


def create_trip(req: Json) -> Tuple[Json, int]:
    return jsonify("test"), 201


def get_trips() -> Tuple[Json, int]:
    return jsonify("test"), 200
