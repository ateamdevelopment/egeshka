from typing import Final

from flask.wrappers import Response
from pytest import exit

from src.urls.exceptions import InvalidTypeException, Error
from src.urls.auth import CheckEmailUrl
from tests.conftest import parameterize, order, TEST_USER_EMAIL
from tests.test_urls.test_auth._responses import (
    ExceptionResponse, TokenResponse, ErrorResponse
)

_EMAIL_TOKEN_NAME: Final[str] = CheckEmailUrl.NAME_TOKEN


def check_email(test_client, email_token, code) -> Response:
    return test_client.post(
        '/auth/check_email',
        data={_EMAIL_TOKEN_NAME: email_token, 'code': code}
    )


# TODO: сделать рандомную генерацию кода и проверку на отличие кодов при 2ух запросах
#   на один email
def get_code(email: str) -> int:
    # noinspection PyProtectedMember
    # noinspection PyUnresolvedReferences
    return CheckEmailUrl._CheckEmailUrl__cache_email_sessions[email].code


@order(4)
def test_check_email_exception(test_client, test_user_email_token):
    assert ExceptionResponse(InvalidTypeException(int, 'code')) == \
           check_email(test_client, test_user_email_token, 'str_code')


@order(5)
@parameterize(
    ['token', 'code', 'expected_response'],
    [[
        'invalid_email_token',
        lambda: get_code(TEST_USER_EMAIL),
        ErrorResponse(Error.NO_SESSION)
    ], [
        None,
        lambda: get_code(TEST_USER_EMAIL) + 1,  # invalid code
        ErrorResponse(CheckEmailUrl.MismatchedCodeError)
    ]]
)
def test_check_email_error(
        test_client, token, code, expected_response, test_user_email_token
):
    assert check_email(test_client, token or test_user_email_token, code()) ==\
           expected_response


@order(6)
def test_check_email_successful(test_client, test_user_email_token):
    try:
        assert TokenResponse(user_token=100) ==\
               check_email(test_client, test_user_email_token, get_code(TEST_USER_EMAIL))
    except AssertionError as assertion_error:
        exit(f'Failed to email confirmation test_user: {assertion_error}')
