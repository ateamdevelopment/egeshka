import base64
from http import HTTPStatus
import json

from tests.conftest import parameterize
from tests.test_urls._responses import (
    ExceptionResponse, ErrorResponse, JsonResponse, SuccessfulResponse
)
from tests.test_urls.test_user_urls.test_user_url import user__get
from src.urls.exceptions import NoParameterException, HTTP_Exception, Error

from flask.wrappers import Response


def avatar__put(test_client, user_token: str, avatar_data: bytes) -> Response:
    return avatar__put__by_data(
        test_client,
        {
            'user_token': user_token,
            'avatar_data': base64.b64encode(avatar_data)
        }
    )


def avatar__put__by_data(test_client, data) -> Response:
    return test_client.put('/user/avatar', data=data)


def avatar__delete(test_client, user_token: str) -> Response:
    return avatar__delete__by_data(test_client, data={'user_token': user_token})


def avatar__delete__by_data(test_client, data) -> Response:
    return test_client.delete('/user/avatar', data=data)


def _get_avatar_url(test_client, user_token) -> str:
    return json.loads(
        user__get(test_client, data={'user_token': user_token}).data
    )['avatar_url']


@parameterize(
    ['data', 'expected_response'],
    [[
        {},
        ExceptionResponse(NoParameterException('avatar_data'))
    ], [
        {'avatar_data': 'avatar data with invalid encoding'},
        ExceptionResponse(HTTP_Exception(
            HTTPStatus.BAD_REQUEST, '`avatar_data` encoding must be base64 (/+)'))
    ], [
        {'avatar_data': base64.b64encode(
            b'avatar data with valid encoding but invalid image data')},
        ExceptionResponse(HTTP_Exception(HTTPStatus.BAD_REQUEST, 'Invalid `avatar_data`'))
    ]]
)
def test__avatar_url__put__exception(
        test_client, test_user_token, data, expected_response):
    assert avatar__put__by_data(
        test_client, data=data | {'user_token': test_user_token}
    ) == expected_response


def test__avatar_url__put__error(test_client, test_image):
    assert avatar__put(test_client, 'invalid_user_token', test_image.read()) == \
           ErrorResponse(Error.NO_SESSION)


def test__avatar_url__put__successful(test_client, test_user_token, test_image):
    assert avatar__put(test_client, test_user_token, test_image.read()) == \
           JsonResponse({'avatar_url': _get_avatar_url(test_client, test_user_token)})


def test__avatar_url__delete__error(test_client):
    assert avatar__delete(test_client, 'invalid_user_token') == \
           ErrorResponse(Error.NO_SESSION)


def test__avatar_url__delete__successful(test_client, test_user_token):
    assert avatar__delete(test_client, test_user_token) == \
           SuccessfulResponse(None)

    assert _get_avatar_url(test_client, test_user_token) is None
