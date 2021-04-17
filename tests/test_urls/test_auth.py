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
        {'email': 'valid_email@mail.ru'},
        ExceptionResponse(NoParameterException('password'))
    ], [
        {'email': 'not_valid_email@.ru', 'password': 'valid_password'},
        ExceptionResponse(HTTP_Exception(
            HTTPStatus.BAD_REQUEST,
            '`email` is invalid'
        ))
    ], [
        {'email': 'valid_email@mail.ru', 'password': 'not_valid_пароль'},
        ExceptionResponse(HTTP_Exception(
            HTTPStatus.BAD_REQUEST,
            '`password` is invalid'
        ))
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
        {'email': 'envy15@mail.ru', 'password': 'valid_password'},
        ErrorResponse(1)
    ], [
        {
            'email': '_'.join(['too_long_email'] * 60) + '@gmail.com',
            'password': 'valid_password'
        },
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
    ['email', 'password'],
    [*[['serge2015555@gmail.com', 'serge2015555_password']] * 2]
)
def test_register_successful(test_client, email, password):
    response: Response = test_client.post(
        '/auth/register',
        data={'email': email, 'password': password}
    )
    assert response == TokenResponse(**{EMAIL_TOKEN_NAME: EMAIL_TOKEN_LENGTH})
    email__token[email] = json.loads(response.data)[EMAIL_TOKEN_NAME]


# TODO: сделать рандомную генерацию кода и проверку на отличие кодов при 2ух запросах
#   на один email
def _get_code(email: str) -> int:
    # noinspection PyProtectedMember
    # noinspection PyUnresolvedReferences
    return CheckEmailUrl._CheckEmailUrl__cache_email_sessions[email].code


@parameterize(
    'email',
    ['serge2015555@gmail.com']
)
def test_check_email(test_client, email):
    token = email__token[email]
    response: Response = test_client.post(
        '/auth/check_email',
        data={EMAIL_TOKEN_NAME: token, 'code': _get_code(email)}
    )
    assert response
