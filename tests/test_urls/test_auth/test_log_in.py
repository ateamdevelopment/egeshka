from src.urls.exceptions import NoParameterException
from src.urls.auth import LogInUrl
from tests.conftest import TEST_USER, parameterize, order
from tests.test_urls._responses import TokenResponse, ExceptionResponse, ErrorResponse


def log_in__get(test_client, email, password):
    return log_in__get__by_data(test_client, data={'email': email, 'password': password})


def log_in__get__by_data(test_client, data):
    return test_client.get('auth/log_in', query_string=data)


@parameterize(
    ['data', 'expected_response'],
    [[
        {'password': 'valid_password'},
        ExceptionResponse(NoParameterException('email'))
    ], [
        {'email': 'valid_email@mail.ru'},
        ExceptionResponse(NoParameterException('password'))
    ]]
)
def test__log_in_url__exception(test_client, data, expected_response):
    assert log_in__get__by_data(test_client, data) == expected_response


@parameterize(
    ['email', 'password', 'expected_response'],
    [[
        'not_exists_email@mail.ru', 'valid_password',
        ErrorResponse(LogInUrl.NotExistsUserError)
    ], [
        TEST_USER['email'], 'mismatched_password',
        ErrorResponse(LogInUrl.MismatchedPasswordError)
    ]]
)
def test__log_in_url__error(test_client, email, password, expected_response):
    assert log_in__get(test_client, email, password) == expected_response


@order(5)
def test__log_in__successful(test_client):
    assert log_in__get(test_client, TEST_USER['email'], TEST_USER['password']) == \
           TokenResponse(user_token=100)
