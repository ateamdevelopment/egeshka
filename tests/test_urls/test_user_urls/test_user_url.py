from flask.wrappers import Response

from src.urls.exceptions import Error, NoParameterException
from src.urls.auth import LogInUrl
from tests.conftest import order, TEST_USER
from tests.test_urls._responses import (
    SuccessfulResponse, ExceptionResponse, ErrorResponse, JsonResponse
)
from tests.test_urls.test_auth.test_log_in import log_in__get


def user__get(test_client, data) -> Response:
    return test_client.get('/user', query_string=data)


def user__delete(test_client, data) -> Response:
    return test_client.delete('/user', data=data)


def test__user_url__get__exception(test_client):
    assert user__get(test_client, data=b'') == \
           ExceptionResponse(NoParameterException('user_token'))


def test__user_url__get__error(test_client):
    assert user__get(test_client, {'user_token': 'invalid_user_token'}) == \
           ErrorResponse(Error.NO_SESSION)


@order(6)
def test__user_url__get__successful(test_client, test_user_token):
    # noinspection PyTypeChecker
    assert user__get(test_client, {'user_token': test_user_token}) == \
           JsonResponse(TEST_USER | {'id': 2, 'avatar_url': None})


def test__user_url__delete__exception(test_client):
    assert user__delete(test_client, data=b'') == \
           ExceptionResponse(NoParameterException('user_token'))


def test__user_url__delete__error(test_client):
    assert user__delete(test_client, {'user_token': 'invalid_user_token'}) == \
           ErrorResponse(Error.NO_SESSION)


@order(-1)
def test__user_url__delete__successful(test_client, test_user_token):
    # noinspection PyTypeChecker
    assert user__delete(test_client, {'user_token': test_user_token}) == \
           SuccessfulResponse(None)

    assert log_in__get(test_client, TEST_USER['email'], TEST_USER['password']) == \
           ErrorResponse(LogInUrl.NotExistsUserError)
