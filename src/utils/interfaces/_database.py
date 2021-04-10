from abc import ABC, abstractmethod

from src.utils.types import TypePrimitives

__all__ = ['Database']


class Database(ABC):
    """
    Util class for sending SQL queries to the database
    """

    @property
    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def execute(
            self,
            query: str,
            values: list[TypePrimitives] = None
    ) -> tuple[tuple, ...]:
        """
        :param query: SQL code
        :param values: values substituted in SQL code
        :return: a tuple of requested tables in the form of tuples,
            if nothing was requested, an empty tuple is returned
        """
        raise NotImplementedError
