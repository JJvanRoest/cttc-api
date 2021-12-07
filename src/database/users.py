from peewee import BigAutoField, BooleanField, CharField, SQL, DateTimeField, ForeignKeyField
from .database import BaseModel
from .company_details import CompanyDetails


class Users(BaseModel):
    id = BigAutoField()
    username = CharField(unique=True)
    password = CharField(null=False)
    password_reset_token = CharField(null=True)
    active = BooleanField(null=False, default=False)

    email = CharField(unique=True)
    company = ForeignKeyField(CompanyDetails, backref='users')

    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL(
        'DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'users'