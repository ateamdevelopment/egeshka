from typing import final

from peewee import TextField
from playhouse.postgres_ext import ArrayField

from src.models.tasks.base_task import BaseTask

__all__ = ['SingleTask']


@final
class SingleTask(BaseTask):
    answer_options: tuple[str] = ArrayField(TextField)
    right_answer: str = TextField()
