from typing import Final, final

from peewee import PostgresqlDatabase
from playhouse.db_url import connect
from psycopg2.extensions import cursor

from src.utils.decorators import check_raises
from src.utils.interfaces import Database

__all__ = ['PostgreSql']


@final
class PostgreSql(Database):
    def __init__(self, database_url: str):
        self._connection: Final[PostgresqlDatabase] = connect(database_url)
        self._cursor: Final[cursor] = self._connection.cursor()

    @property
    def connect(self):
        return self._connection

    @check_raises
    def execute(self, query, values=None):
        self._cursor.execute(query=query, vars=values)
        self._connection.commit()
        if self._cursor.pgresult_ptr is None:
            return ()
        return tuple(self._cursor.fetchall())
