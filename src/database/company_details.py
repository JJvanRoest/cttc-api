from peewee import BigAutoField, TextField, DateTimeField, SQL
from .database import BaseModel

class CompanyDetails(BaseModel):
    """
    Company model
    """
    id = BigAutoField()
    name = TextField(null=False)
    location = TextField(null=False)
    
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'company'