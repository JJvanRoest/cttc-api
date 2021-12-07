import inspect
import logging
import sys

from src import database
from peewee import Model


class InvalidArgumentError(ValueError):
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        arg = sys.argv[1]
    except IndexError:
        raise InvalidArgumentError(
            "No argument sent. Send '--build' to build database tables or '--drop' to drop all tables.")
    with database.database as db:
        models = []
        # Don't forget to include the newly created model in database.__init__.py!
        class_members = inspect.getmembers(
            sys.modules[database.__name__], inspect.isclass)
        print(class_members)
        for name, obj in class_members:
            if issubclass(obj, database.BaseModel) and \
                    obj is not database.BaseModel and \
                    obj is not Model:
                models.append(obj)
        print(models)
        if arg == "--build":
            db.create_tables(models)
        elif arg == "--drop":
            db.drop_tables(models)
        else:
            raise InvalidArgumentError(
                "Incorrect argument sent. Send '--build' to build database tables or '--drop' to drop all tables.")
