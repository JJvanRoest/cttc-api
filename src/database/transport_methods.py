from peewee import BigAutoField, CharField, TextField, DateTimeField, SQL
from .database import BaseModel

class TransportMethods(BaseModel):
    id = BigAutoField()
    name = CharField(max_length=255)
    description = TextField(max_length=255)

    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    
    class Meta:
        table_name = 'transport_methods'