from peewee import BigAutoField, ForeignKeyField, IntegerField, CharField
from .database import BaseModel
from .orders import Orders
from .transport_methods import TransportMethods
class OrderItems(BaseModel):
    id = BigAutoField()
    order_id = ForeignKeyField(Orders, backref='order_items')
    name = CharField()
    amount = IntegerField()
    sku = CharField()
    transport_method = ForeignKeyField(TransportMethods, backref='transport_methods')

    class Meta:
        table_name = 'order_items'
