from src.utils import database


def test_select():
    assert (1,) in database.execute(f'SELECT id FROM "user"')
