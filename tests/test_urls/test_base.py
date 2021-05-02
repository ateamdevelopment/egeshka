from http import HTTPStatus

from flask.wrappers import Response

from src.urls.exceptions import HTTP_Exception
from tests.conftest import parameterize
from tests.test_urls._responses import ExceptionResponse


def echo__get__by_data(test_client, data) -> Response:
    return test_client.get('/echo', data=data)


@parameterize(
    ['data', 'expected_response'],
    [[
        '{"bad": "encoding"}'.encode('ISO-8859-1'),
        ExceptionResponse(HTTP_Exception(
            HTTPStatus.BAD_REQUEST, 'The encoding must be UTF-8'))
    ], [
        'bad JSON'.encode(),
        ExceptionResponse(HTTP_Exception(HTTPStatus.BAD_REQUEST, 'Bad JSON'))
    ]]
)
def test__echo__get__exception(test_client, data, expected_response):
    assert echo__get__by_data(test_client, data) == expected_response
