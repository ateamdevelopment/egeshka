from http import HTTPStatus
from typing import Final
import json

from flask.wrappers import Response

from src.urls.exceptions import HTTPException, NoParameterException
from src.urls.auth import CheckEmailUrl
from tests.conftest import parameterize
from tests.test_urls.utils import ExceptionResponse, TokenResponse


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
        ExceptionResponse(HTTPException(
            HTTPStatus.BAD_REQUEST,
            '`email` is not valid'
        ))
    ], [
        {'email': 'valid_email@mail.ru', 'password': 'not_valid_пароль'},
        ExceptionResponse(HTTPException(
            HTTPStatus.BAD_REQUEST,
            '`password` is not valid'
        ))
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
    [
        ['serge2015555@gmail.com', 'serge2015555_password']
    ]
)
def test_register_successful(test_client, email, password):
    response: Response = test_client.post(
        '/auth/register',
        data={'email': email, 'password': password}
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
