from peewee import ForeignKeyField, IntegerField
from .database import BaseModel
from .company import Company

class DistributionCenter(BaseModel):
    company_id = ForeignKeyField(Company, backref='distribution_centers')
    amnt_trucks_waiting = IntegerField(default=0)
    capacity = IntegerField(default=0)
    class Meta:
        table_name = 'distribution_center'