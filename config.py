import json
import os
from datetime import datetime, date

from peewee import Model, ModelSelect
from playhouse.shortcuts import model_to_dict

import logging
from typing import Optional


class _Config:
    def __init__(self):
        file_name = "config.json"
        self.config_file = os.path.join(os.path.dirname(__file__), file_name)
        with open(self.config_file) as f:
            self._config_dict = json.load(f)

    @property
    def database(self) -> dict:
        return self.get_config("database")

    def get_config(self, key: Optional[str]) -> dict:
        if key is None:
            return self._config_dict
        return self._config_dict[key]


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            elif isinstance(obj, Model):
                return model_to_dict(obj)
            elif isinstance(obj, ModelSelect):
                return [model_to_dict(item) for item in obj]
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return json.JSONEncoder.default(self, obj)

CONFIG = _Config()