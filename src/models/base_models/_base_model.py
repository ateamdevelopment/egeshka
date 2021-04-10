from __future__ import annotations

from abc import ABC

from peewee import Model
from playhouse.shortcuts import model_to_dict

from src.utils import database as util_database
from src.utils.types import TypeJson

__all__ = ['BaseModel']


class _MetaBaseModel(type(Model), type(ABC)):
    pass


class BaseModel(Model, ABC, metaclass=_MetaBaseModel):
    """
    Base class for database models. Any model does not have a public __init__
    """

    class Meta:
        database = util_database.connect

    @staticmethod
    def execute(query: str, values=None) -> tuple[tuple, ...]:
        return util_database.execute(query, values)

    def serialize(self) -> TypeJson:
        return model_to_dict(self)

    def __str__(self) -> str:
        return str(self.serialize())

    def __repr__(self) -> str:
        return str(self)
