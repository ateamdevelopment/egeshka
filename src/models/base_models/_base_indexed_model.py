from __future__ import annotations

from abc import ABC
from typing import Final

from peewee import IntegerField

from src.models.base_models._base_model import BaseModel

__all__ = ['BaseIndexedModel']


class BaseIndexedModel(BaseModel, ABC):
    id: Final[int] = IntegerField(primary_key=True)

    @classmethod
    def get_by_id(cls, id: int) -> BaseIndexedModel:
        return super().get(id=id)
