from peewee import BigAutoField, CharField, TextField, DateTimeField, SQL
from .database import BaseModel


class CompanyDetails(BaseModel):
    """
    Company model
    """
    id = BigAutoField()
    name = TextField(null=False)
    location = TextField(null=False)

    api_key = CharField(null=False, unique=True)

    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL(
        'DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'company'
