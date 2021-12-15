from peewee import BigAutoField, CharField, TextField, DateTimeField, SQL
from .database import BaseModel


class Company(BaseModel):
    """
    Company model
    """
    id = BigAutoField()
    company_name = TextField(null=False)
    company_location = TextField(null=False)
    company_type = CharField(null=False)
    company_api_url = TextField(null=False)

    api_key = CharField(null=False, unique=True)

    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL(
        'DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'company'
