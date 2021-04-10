from typing import final

from playhouse.postgres_ext import JSONField

from src.models.tasks.base_task import BaseTask
from src.utils.types import TypeJson

__all__ = ['MapTask']


@final
class MapTask(BaseTask):
    map: TypeJson = JSONField()
