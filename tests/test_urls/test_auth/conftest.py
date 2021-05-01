from pytest import fixture

from tests.conftest import TEST_USER
from tests.test_urls.test_auth.test_register import get_email_token


@fixture(scope='module')
def test_user_email_token(test_client):
    return get_email_token(test_client, **TEST_USER)
