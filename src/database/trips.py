from peewee import BigAutoField, BooleanField, DateTimeField, ForeignKeyField, IntegerField, CharField, SQL, BitField
from datetime import datetime
from .database import BaseModel
from .company import Company
from playhouse.postgres_ext import JSONField


class Trips(BaseModel):
    id = BigAutoField()
    uuid = CharField(unique=True)
    # Locations format: `Street> <House Number>, <City>, <Country>`
    start_location = CharField()
    start_gps_location = CharField()
    pickup_location = CharField()
    pickup_gps_location = CharField()
    destination_location = CharField()
    destination_gps_location = CharField()
    truck_location = CharField()
    truck_gps_location = CharField()
    truck_license_plate = CharField()
    current_truck_load = IntegerField()
    payload = JSONField()

    dist_center = ForeignKeyField(Company, backref='trips')
    truck_company = ForeignKeyField(Company, backref='trips')

    kms_travelled = IntegerField()
    ready_for_pickup = BooleanField()
    exp_eta = DateTimeField()

    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'trips'
