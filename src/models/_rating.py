from typing import final

from peewee import ForeignKeyField, CompositeKey, IntegerField

from src.models._subject import Subject
from src.models._user import User
from src.models.base_models import BaseModel

__all__ = ['Rating']


@final
class Rating(BaseModel):
    """
    CREATE TABLE rating (
    user_id Integer NOT NULL
        REFERENCES "user"
            ON DELETE CASCADE,
    subject_id Smallint NOT NULL
        REFERENCES subject
            ON DELETE CASCADE,
    elo Integer NOT NULL,

    PRIMARY KEY (user_id, subject_id)
    );
    """

    class Meta:
        primary_key = CompositeKey('user_id', 'subject_id')

    user_id: int = ForeignKeyField(User)
    subject_id: int = ForeignKeyField(Subject)
    elo: int = IntegerField()
