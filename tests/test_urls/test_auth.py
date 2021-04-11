from http import HTTPStatus

from flask.wrappers import Response

from src.urls.exceptions import HTTPException, NoParameterException
from tests.conftest import parameterize
from tests.test_urls.utils import ExceptionResponse


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
def test_register(test_client, test_data, expect_response):
    response: Response = test_client.post(
        '/auth/register',
        data=test_data
    )
    assert expect_response == response
