from http import HTTPStatus
from typing import Final
import json

from flask.wrappers import Response
from pytest import exit

from src.urls.exceptions import HTTP_Exception, NoParameterException
from src.urls.auth import CheckEmailUrl, RegisterUrl
from tests.conftest import parameterize, order, TEST_USER_EMAIL, TEST_USER_PASSWORD
from tests.test_urls.test_auth._responses import (
    ExceptionResponse, TokenResponse, ErrorResponse
)

__all__ = ['get_email_token']

_EMAIL_TOKEN_NAME: Final[str] = CheckEmailUrl.NAME_TOKEN
_EMAIL_TOKEN_LENGTH: Final[int] = CheckEmailUrl.LENGTH_TOKEN


def register_by_data(test_client, data) -> Response:
    return test_client.post('/auth/register', data=data)


def register(test_client, email: str, password: str) -> Response:
    return register_by_data(test_client, {'email': email, 'password': password})


def get_email_token(test_client, email: str, password: str) -> str:
    return json.loads(register(test_client, email, password).data)[_EMAIL_TOKEN_NAME]


@order(1)
@parameterize(
    ['test_data', 'expected_response'],
    [[
        b'', ExceptionResponse(NoParameterException('email'))
    ], [
        {'email': 'valid_email@mail.ru'},
        ExceptionResponse(NoParameterException('password'))
    ], [
        {'email': 'invalid_email@.ru', 'password': 'valid_password'},
        ExceptionResponse(HTTP_Exception(HTTPStatus.BAD_REQUEST, '`email` is invalid'))
    ], [
        {'email': 'valid_email@mail.ru', 'password': 'invalid_пароль'},
        ExceptionResponse(HTTP_Exception(HTTPStatus.BAD_REQUEST, '`password` is invalid'))
    ]]
)
def test_register_exceptions(test_client, test_data, expected_response):
    assert expected_response == register_by_data(test_client, test_data)


@order(2)
@parameterize(
    ['email', 'password', 'expected_response'],
    [[
        'envy15@mail.ru', 'valid_password',
        ErrorResponse(RegisterUrl.NonUniqueEmailError)
    ], [
        '_'.join(['too_long_email'] * 60) + '@gmail.com', 'valid_password',
        ErrorResponse(RegisterUrl.SendEmailError)
    ]]
)
def test_register_errors(test_client, email, password, expected_response):
    assert expected_response == register(test_client, email, password)


@order(3)
def test_register_successful(test_client):
    try:
        assert TokenResponse(**{_EMAIL_TOKEN_NAME: _EMAIL_TOKEN_LENGTH}) == \
               register(test_client, TEST_USER_EMAIL, TEST_USER_PASSWORD)
    except AssertionError as assertion_error:
        exit('Failed to register test_user: ', assertion_error)
