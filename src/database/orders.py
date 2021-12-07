from peewee import BigAutoField, BooleanField, DateTimeField, ForeignKeyField, IntegerField, CharField, SQL

from .database import BaseModel
from .distribution_center import DistributionCenter as DC
from .truck_company import TruckCompany as TC


class Orders(BaseModel):
    id = BigAutoField()
    amnt_cargo = IntegerField()
    dist_center = ForeignKeyField(DC, backref='orders')
    truck_company = ForeignKeyField(TC, backref='orders')
    end_loc = CharField()
    kms_travelled = IntegerField()
    ready_for_pickup = BooleanField()
    exp_delivery_date = DateTimeField()
    pickup_date = DateTimeField()

    created_at = DateTimeField(
        constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL(
        'DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'orders'
