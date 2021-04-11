import atexit
import os
from typing import Final

from src import DATABASE_URL

DEFAULT_DUMP_NAME: Final[str] = 'db.dump'


def init_backup() -> None:
    f"""
    Requires dump file - db.dump and PostgreSQL.
    
    To create db.dump, run the command:
        pg_dump --dbname={DATABASE_URL} --format=custom --clean > {DEFAULT_DUMP_NAME}
    """
    _restore(DEFAULT_DUMP_NAME)
    atexit.register(_restore, DEFAULT_DUMP_NAME)


def _restore(dump_name: str) -> None:
    assert os.system(
        f'pg_restore'
        f'  --dbname={DATABASE_URL}'
        f'  --format=custom'
        f'  --clean '
        f'{os.getcwd()}\\{dump_name}'
    ) == 0
