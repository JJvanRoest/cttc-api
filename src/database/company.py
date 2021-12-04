from peewee import BigAutoField, TextField
from .database import BaseModel

class Company(BaseModel):
    """
    Company model
    """
    id = BigAutoField()
    name = TextField(null=False)
    location = TextField(null=False)
    company_type = 


    class Meta:
        table_name = 'company'