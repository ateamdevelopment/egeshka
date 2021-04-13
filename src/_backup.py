from typing import Final
import os

from src import DATABASE_URL

DUMP_FILENAME: Final[str] = 'db.dump'


def init_backup() -> None:
    f"""
    To create db.dump, run the command:
        pg_dump --dbname={DATABASE_URL} --format=custom > db.dump
    """
    os.system(
        f'pg_restore'
        f'  --dbname={DATABASE_URL}'
        f'  --format=custom'
        f'  --clean '
        f'{DUMP_FILENAME}'
    )
