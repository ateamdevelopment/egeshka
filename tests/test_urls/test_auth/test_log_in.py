from flask import Response

from tests.conftest import TEST_USER
from tests.test_urls._responses import TokenResponse


def log_in__get(test_client, email, password) -> Response:
    return test_client.get(
        '/auth/log_in',
        query_string={'email': email, 'password': password}
    )


def test__log_in__successful(test_client):
    assert TokenResponse(user_token=100) == \
           log_in__get(test_client, TEST_USER['email'], TEST_USER['password'])
