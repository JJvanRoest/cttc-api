from peewee import DateTimeField, Model, PostgresqlDatabase
import peewee as pw
from playhouse.shortcuts import ReconnectMixin
import logging
from config import CONFIG
from datetime import datetime
from playhouse.postgres_ext import *


class ReconnectDatabase(ReconnectMixin, PostgresqlExtDatabase):
    pass


logging.info(CONFIG.database)
database = ReconnectDatabase(
    database=CONFIG.database["database"],
    host=CONFIG.database["host"],
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
