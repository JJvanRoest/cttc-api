from pydantic.dataclasses import dataclass as pydantic_dataclass, is_builtin_dataclass
from pydantic import ValidationError
from pydantic.types import Json
from werkzeug.exceptions import BadRequest

from enum import Enum

from typing import Union


class ExtendedEnum(Enum):
    """
    Adds list conversion to enum names.
    """
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class RequestSchemaValidationError(BadRequest):
    def __init__(self, validation_error: Union[TypeError, ValidationError]) -> None:
        super().__init__()
        self.validation_error = validation_error


def validate_request(model, source: Json) -> bool:
    model_class = pydantic_dataclass(model)
    try:
        model = model_class(**source)
    except (TypeError, ValidationError) as error:
        raise RequestSchemaValidationError(error)
    return True
