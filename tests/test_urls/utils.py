from typing import Optional, Final, Union
import json

from flask.wrappers import Response

from src.utils.types import TypeJson
from src.urls.exceptions import HTTPException


class TestResponse:
    def __init__(self, status: int, data: Optional[bytes] = b''):
        self.status: Final[int] = status
        self.data: Final[Optional[bytes]] = data

    def __eq__(self, response: Response):
        return self._eq_status(response.status_code) and self._eq_data(response.data)

    def _eq_status(self, response_status: int) -> bool:
        return self.status == response_status

    def _eq_data(self, response_data: bytes) -> bool:
        if self.data is None:
            return True
        print(self.data)
        print(response_data)
        return self.data == response_data


class SuccessfulResponse(TestResponse):
    def __init__(self, data=b''):
        TestResponse.__init__(self, 200, data)

    def _eq_status(self, response_status):
        return response_status < 500


class JsonResponse(SuccessfulResponse):
    def __init__(self, data: Optional[Union[bytes, TypeJson]]):
        if isinstance(data, bytes):
            SuccessfulResponse.__init__(self, data)
            json_data = json.loads(data)
        else:
            SuccessfulResponse.__init__(self, json.dumps(data).encode())
            json_data = data
        self.json: Final[TypeJson] = json_data

    def _eq_data(self, response_data):
        if self.data is None:
            return True
        return self.json == json.loads(response_data)


class TokenResponse(JsonResponse):
    def __init__(self, data, **token_name__length: int):
        JsonResponse.__init__(self, data)
        self.token_name__length: Final[dict[str, int]] = token_name__length

    def _eq_data(self, response_data):
        if super()._eq_data(response_data):
            return all(
                len(token) == self.token_name__length[token]
                if (token := self.json.get(token_name)) else False
                for token_name in self.token_name__length
            )


class ErrorResponse(JsonResponse):
    def __init__(self, error_code: int):
        JsonResponse.__init__(self, {'error': error_code})


class ExceptionResponse(TestResponse):
    def __init__(self, http_exception: HTTPException):
        TestResponse.__init__(
            self,
            http_exception.http_status,
            str(http_exception).encode()
        )
