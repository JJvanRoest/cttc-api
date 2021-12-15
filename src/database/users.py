from datetime import datetime
from peewee import BigAutoField, BooleanField, CharField, SQL, DateTimeField, ForeignKeyField
from .database import BaseModel
from .company import Company


class Users(BaseModel):
    id = BigAutoField()
    username = CharField(null=False)
    password = CharField(null=False)
    password_reset_token = CharField(null=True)
    active = BooleanField(null=False, default=True)

    email = CharField(unique=True)
    company = ForeignKeyField(Company, backref='users')

    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    class Meta:
        table_name = 'users'
