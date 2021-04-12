from typing import Final
import os

from src import DATABASE_URL


DUMP_FILENAME: Final[str] = 'db.dump'


def init_backup():
    os.system(
        f'pg_restore'
        f'  --dbname={DATABASE_URL}'
        f'  --format=custom'
        f'  --clean '
        f'{DUMP_FILENAME}'
    )
