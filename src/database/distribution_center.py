from peewee import BigAutoField, ForeignKeyField, IntegerField
from .database import BaseModel
from .company_details import CompanyDetails

class DistributionCenter(BaseModel):
    id  = BigAutoField()
    company_id = ForeignKeyField(CompanyDetails, backref='distribution_centers')
    amnt_trucks_waiting = IntegerField(default=0)
    capacity = IntegerField(default=0)
    class Meta:
        table_name = 'distribution_center'