import json
import httpx
from config import CONFIG
from datetime import datetime
from playhouse.shortcuts import dict_to_model, model_to_dict
from uuid import uuid4, UUID
from typing import List, Dict, Tuple
from dataclasses import dataclass
from pydantic.types import Json
from quart import Blueprint, request, jsonify
import asyncio
from ...database.trips import Trips
from ...database.database import database as db
from ...database.company import Company

from ..helpers.validation import validate_request, ExtendedEnum

trips_endpoints = Blueprint('trips_endpoints', __name__)


class CargoTypes(ExtendedEnum):
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
    payload: List[Dict]
    truck_license_plate: str
    truck_location: str
    current_truck_load: int


@trips_endpoints.route('/', methods=['GET', 'POST'])
async def trips():
    if request.method == "POST":
        req = await request.get_json()
        print(req)
        validate_request(model=TripRequestSchema, source=req)
        res = await create_trip(req)
        return res
    else:
        return get_trips()


async def create_trip(req: Json) -> Tuple[Json, int]:
    company_name, license_plate = parse_license_plate(
        req['truck_license_plate'])
    payload_ok = verify_payload(req['payload'])

    start_location = req["start_location"]
    pickup_location = req["pickup_location"]
    destination_location = req["destination_location"]

    start_gps_location, pickup_gps_location, destination_gps_location = await asyncio.gather(
        get_gps_coordinates(start_location),
        get_gps_coordinates(pickup_location),
        get_gps_coordinates(destination_location)
    )
    truck_company = Company.get_or_none(Company.company_name == company_name)
    dist_center = Company.get_or_none(
        Company.company_location == pickup_location)
    truck_gps_location = start_gps_location

    if truck_company is None:
        return jsonify({"error": "Please register your company before creating trips."}), 400
    if dist_center is None:
        return jsonify({"error": "Pickup location could not be matched to a distribution center."}), 400

    if not payload_ok:
        return jsonify({"error": "Invalid payload"}), 400
    with db.atomic():
        trip = Trips.create(
            uuid=req["id"],
            start_location=req["start_location"],
            start_gps_location=start_gps_location,
            pickup_location=req["pickup_location"],
            pickup_gps_location=pickup_gps_location,
            destination_location=req["destination_location"],
            destination_gps_location=destination_gps_location,
            truck_license_plate=license_plate,
            truck_location=req["truck_location"],
            truck_gps_location=truck_gps_location,
            current_truck_load=req["current_truck_load"],
            payload=req["payload"],

            dist_center=dist_center,
            truck_company=truck_company,
            kms_travelled=0,

            ready_for_pickup=True,
            exp_eta=datetime.now()
        )
    trip_dict = model_to_dict(trip)
    return jsonify({"success": trip_dict}), 201


def parse_license_plate(license_plate: str) -> Tuple[str, str]:
    license_tokens = license_plate.split("-", 1)
    if not len(license_tokens) == 2:
        raise ValueError("Invalid license plate")
    return license_tokens[0], license_tokens[1]


def verify_payload(payload: List[Dict]) -> bool:
    cargo_types = CargoTypes.list()
    for item in payload:
        try:
            if not item["cargo_type"] in cargo_types:
                return False
        except TypeError:
            return False
    return True


def get_trips() -> Tuple[Json, int]:
    trips_dict: List[Dict] = []
    trips = Trips.select()
    for trip in trips:
        trip_dict: Dict = model_to_dict(trip)
        trips_dict.append(trip_dict)
    return jsonify({"trips": trips_dict}), 200


async def get_gps_coordinates(location: str) -> str:
    if CONFIG.ext_api["test_mode"] == True:
        return test_response()

    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"http://api/positionstack/com/v1/forward?query={location}&access_key={CONFIG.ext_api['positionstack_token']}")
    return res.json()


def test_response() -> str:
    return "40.755884,-73.978504"
