from peewee import BigAutoField, BooleanField, DateTimeField, ForeignKeyField, IntegerField, CharField, SQL, BitField, FloatField
from datetime import datetime
from .database import BaseModel
from .company import Company
from playhouse.postgres_ext import JSONField


class Locations(BaseModel):
    id = BigAutoField()
    location = CharField()
    location_data = JSONField()

    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'locations'
