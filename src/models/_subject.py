from __future__ import annotations

from typing import final

from peewee import TextField

from src.models.base_models import BaseIndexedModel, BaseModelEnum

__all__ = ['Subject']


@final
class Subject(BaseIndexedModel, BaseModelEnum):
    """
    CREATE TABLE subject (
        id Smallint
            PRIMARY KEY,
        name Text NOT NULL
            UNIQUE
            CHECK (name != '')
    );
    """

    MATHEMATICS: Subject
    RUSSIAN_LANGUAGE: Subject

    @classmethod
    def _init_static(cls):
        cls.RUSSIAN_LANGUAGE = cls.get(id=1)
        cls.MATHEMATICS = cls.get(id=2)

    name: str = TextField()

    @classmethod
    def get_by_id(cls, id) -> Subject:
        return super().get_by_id(id)

    @classmethod
    def get_by_name(cls, name: str) -> Subject:
        return super().get(name=name)
