from typing import Final
import os

from testfixtures import TempDirectory
import pytest
from pytest import fixture

from src.app import app

__import__('src.main')

mark: Final = pytest.mark
parameterize: Final = mark.parametrize
order: Final = mark.order


@fixture(scope='session')
def test_client():
    testing_client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@fixture()
def temp_dir():
    with TempDirectory() as temp_directory:
        yield temp_directory


@fixture()
def temp_text_file(temp_dir):
    with open(os.path.join(temp_dir.path, 'temp_text_file.txt'), 'w+') as temp_file:
        yield temp_file


@fixture(scope='session')
def _test_image():
    with open(os.getcwd() + '/tests/resources/test_image.jpg', 'rb') as test_image_:
        yield test_image_


@fixture(scope='function')
def test_image(_test_image):
    _test_image.seek(0)
    return _test_image


TEST_USER_EMAIL: Final[str] = 'serge2015555@gmail.com'
TEST_USER_PASSWORD: Final[str] = 'serge2015555_password'


@fixture(scope='session')
def test_user(test_client):
    token = test_client.get(

    )