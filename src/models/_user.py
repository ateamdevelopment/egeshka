from __future__ import annotations

from typing import final

from peewee import TextField

from src.models.base_models import BaseIndexedModel

__all__ = ['User']


@final
class User(BaseIndexedModel):
    r"""
    CREATE TABLE "user" (
        id Serial NOT NULL
            PRIMARY KEY,
        email Text NOT NULL
            UNIQUE
            CHECK (email ~ '^[a-zA-Z0-9]+([-._][a-zA-Z0-9]+)*@[a-zA-Z0-9]+([-.][
                            a-zA-Z0-9]+)*\.[a-zA-Z]{2,7}$',
        password Text NOT NULL
            CHECK (password ~ '^[a-zA-z0-9_]{6,}$'),
        avatar_url Text
            CHECK (avatar_url ~ 'https?://.+')
    );
    """

    email: str = TextField()
    password: str = TextField()
    avatar_url: str = TextField()

    @classmethod
    def get_by_id(cls, id) -> User:
        return super().get_by_id(id)

    @classmethod
    def get_by_email(cls, email: str) -> User:
        return super().get(email=email)

    @classmethod
    def create(cls, email: str, password: str, avatar_url: str = None) -> User:
        return super().create(email=email, password=password, avatar_url=avatar_url)
