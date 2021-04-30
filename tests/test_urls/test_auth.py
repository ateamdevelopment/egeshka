from http import HTTPStatus
from typing import Final
import json

from flask.wrappers import Response

from src.urls.exceptions import HTTP_Exception, NoParameterException
from src.urls.auth import CheckEmailUrl
from tests.conftest import parameterize
from tests.test_urls.utils import ExceptionResponse, TokenResponse, ErrorResponse

EMAIL_TOKEN_NAME: Final[str] = CheckEmailUrl.NAME_TOKEN
EMAIL_TOKEN_LENGTH: Final[int] = CheckEmailUrl.LENGTH_TOKEN


@parameterize(
    ['test_data', 'expect_response'],
    [[
        b'',
        ExceptionResponse(NoParameterException('email'))
    ], [
        {'email': 'valid_email@mail.ru', 'first_name': 'Валидноеимя',
         'last_name': 'Валиднаяфамилия'},
        ExceptionResponse(NoParameterException('password'))
    ], [
        {'email': 'valid_email@mail.ru', 'password': 'valid_password',
         'last_name': 'Валиднаяфамилия'},
        ExceptionResponse(NoParameterException('first_name'))
    ], [
        {'email': 'valid_email@mail.ru', 'password': 'valid_password',
         'first_name': 'Валидноеимя'},
        ExceptionResponse(NoParameterException('last_name'))
    ], [
        {'email': 'not_valid_email@.ru', 'password': 'valid_password',
         'first_name': 'Валидноеимя', 'last_name': 'Валиднаяфамилия'},
        ExceptionResponse(HTTP_Exception(HTTPStatus.BAD_REQUEST, '`email` is invalid'))
    ], [
        {'email': 'valid_email@mail.ru', 'password': 'not_valid_пароль',
         'first_name': 'Валидноеимя', 'last_name': 'Валиднаяфамилия'},
        ExceptionResponse(HTTP_Exception(HTTPStatus.BAD_REQUEST, '`password` is invalid'))
    ], [
        {'email': 'valid_email@mail.ru', 'password': 'valid_password',
         'first_name': '', 'last_name': 'Валиднаяфамилия'},
        ExceptionResponse(HTTP_Exception(
            HTTPStatus.BAD_REQUEST, '`first_name` is invalid'))
    ], [
        {'email': 'valid_email@mail.ru', 'password': 'valid_password',
         'first_name': 'Валидноеимя', 'last_name': ''},
        ExceptionResponse(HTTP_Exception(
            HTTPStatus.BAD_REQUEST, '`last_name` is invalid'))
    ]]
)
def test_register_exceptions(test_client, test_data, expect_response):
    response: Response = test_client.post(
        '/auth/register',
        data=test_data
    )
    assert expect_response == response


@parameterize(
    ['test_data', 'expect_response'],
    [[
        {'email': 'envy15@mail.ru', 'password': 'valid_password',
         'first_name': 'Валидноеимя', 'last_name': 'Валиднаяфамилия'},
        ErrorResponse(1)
    ], [
        {'email': '_'.join(['too_long_email'] * 60) + '@gmail.com',
         'password': 'valid_password', 'first_name': 'Валидноеимя',
         'last_name': 'Валиднаяфамилия'},
        ErrorResponse(2)
    ]]
)
def test_register_errors(test_client, test_data, expect_response):
    response: Response = test_client.post(
        '/auth/register',
        data=test_data
    )
    assert expect_response == response


email__token: Final[dict[str, str]] = {}


@parameterize(
    ['email', 'password', 'first_name', 'last_name'],
    [*[['serge2015555@gmail.com', 'serge2015555_password', 'Валидноеимя',
        'Валиднаяфамилия']] * 2]
)
def test_register_successful(test_client, email, password, first_name, last_name):
    response: Response = test_client.post(
        '/auth/register',
        data={
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
    )
    assert response == TokenResponse(**{EMAIL_TOKEN_NAME: EMAIL_TOKEN_LENGTH})
    email__token[email] = json.loads(response.data)[EMAIL_TOKEN_NAME]


@parameterize(
    'email',
    ['serge2015555@gmail.com']
)
def test_check_email(test_client, email):
    token = email__token[email]
    response: Response = test_client.post(
        '/auth/check_email',
        data={EMAIL_TOKEN_NAME: token, 'code': 1000}
    )
    assert response
