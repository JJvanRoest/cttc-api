from peewee import BigAutoField, IntegerField
from .database import BaseModel

class TruckCompany(BaseModel):
    id = BigAutoField()
    amnt_trips_done = IntegerField(null=False, default=0)

    class Meta:
        table_name = 'truck_company'