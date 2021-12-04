from peewee import Model, PostgresqlDatabase
from playhouse.shortcuts import ReconnectMixin
import logging
from config import CONFIG

class ReconnectDatabase(ReconnectMixin, PostgresqlDatabase):
    pass

logging.info(CONFIG.database)
database = PostgresqlDatabase(
    database = CONFIG.database["database"], 
    host = CONFIG.database["host"],
    port=CONFIG.database["port"],
    user=CONFIG.database["user"],
    password=CONFIG.database["password"],
    )

class UnknownField(object):
    def __init__(self, *_, **__): 
        # Placeholder used in case Peewee doesn't know how to map to a field class
        pass

class BaseModel(Model):
    class Meta:
        database = database
