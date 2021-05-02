from http import HTTPStatus
from typing import Final
import json

from flask.wrappers import Response
from pytest import exit

from src.urls.exceptions import HTTP_Exception, NoParameterException
from src.urls.auth import CheckEmailUrl, RegisterUrl
from tests.conftest import parameterize, order, TEST_USER
from tests.test_urls._responses import (
    ExceptionResponse, TokenResponse, ErrorResponse
)

_EMAIL_TOKEN_NAME: Final[str] = CheckEmailUrl.NAME_TOKEN
_EMAIL_TOKEN_LENGTH: Final[int] = CheckEmailUrl.LENGTH_TOKEN


def get_email_token(
        test_client, email: str, password: str, first_name: str, last_name: str
) -> str:
    return json.loads(register__post(
        test_client, email, password, first_name, last_name
    ).data)[_EMAIL_TOKEN_NAME]


def register__post(
        test_client, email: str, password: str, first_name: str, last_name: str
) -> Response:
    return register__post__by_data(test_client, {
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name
    })


def register__post__by_data(test_client, data) -> Response:
    return test_client.post('/auth/register', data=data)


def _test_user_without_item(item: str):
    return _copy_dict_without_item(TEST_USER, item)


def _copy_dict_without_item(dictionary: dict, item: str):
    new_dict = dictionary.copy()
    del new_dict[item]
    return new_dict


@parameterize(
    ['test_data', 'expected_response'],
    [[
        b'',
        ExceptionResponse(NoParameterException('email'))
    ], [
        _test_user_without_item('email'),
        ExceptionResponse(NoParameterException('email'))
    ], [
        _test_user_without_item('password'),
        ExceptionResponse(NoParameterException('password'))
    ], [
        _test_user_without_item('first_name'),
        ExceptionResponse(NoParameterException('first_name'))
    ], [
        _test_user_without_item('last_name'),
        ExceptionResponse(NoParameterException('last_name'))
    ], [
        TEST_USER | {'email': 'not_valid_email@.ru'},
        ExceptionResponse(HTTP_Exception(HTTPStatus.BAD_REQUEST, '`email` is invalid'))
    ], [
        TEST_USER | {'password': 'not_valid_пароль'},
        ExceptionResponse(HTTP_Exception(HTTPStatus.BAD_REQUEST, '`password` is invalid'))
    ], [
        TEST_USER | {'first_name': ''},
        ExceptionResponse(HTTP_Exception(
            HTTPStatus.BAD_REQUEST, '`first_name` is invalid'))
    ], [
        TEST_USER | {'last_name': ''},
        ExceptionResponse(HTTP_Exception(
            HTTPStatus.BAD_REQUEST, '`last_name` is invalid'))
    ]]
)
def test__register__exceptions(test_client, test_data, expected_response):
    assert expected_response == register__post__by_data(test_client, test_data)


@parameterize(
    ['email', 'password', 'first_name', 'last_name', 'expected_response'],
    [[
        'envy15@mail.ru', 'valid_password', 'Валидноеимя', 'Валиднаяфамилия',
        ErrorResponse(RegisterUrl.NonUniqueEmailError)
    ], [
        '_'.join(['too_long_email'] * 60) + '@gmail.com',
        'valid_password', 'Валидноеимя', 'Валиднаяфамилия',
        ErrorResponse(RegisterUrl.SendEmailError)
    ]]
)
def test__register__errors(
        test_client, email, password, first_name, last_name, expected_response
):
    assert expected_response == register__post(
        test_client, email, password, first_name, last_name
    )


@order(1)
def test__register__successful(test_client):
    try:
        assert TokenResponse(**{_EMAIL_TOKEN_NAME: _EMAIL_TOKEN_LENGTH}) == \
               register__post(test_client, **TEST_USER)
    except AssertionError as assertion_error:
        exit('Failed to register test_user: ' + str(assertion_error))
