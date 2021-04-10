from http import HTTPStatus
from typing import Union, Final

__all__ = ['HTTPException']

_HTTP_CODE_STATUS: dict[int, HTTPStatus] = {
    http_status.value: http_status for http_status in HTTPStatus
}


class HTTPException(Exception):
    def __init__(
            self,
            http_status: Union[int, HTTPStatus] = HTTPStatus.INTERNAL_SERVER_ERROR,
            message: str = ''
    ):
        self.http_status: Final[HTTPStatus] = _HTTP_CODE_STATUS[http_status] if \
            isinstance(http_status, int) else http_status
        self.message: Final[str] = message

    def __str__(self) -> str:
        return f'{self.http_status.phrase} ({self.http_status.value}): ' \
               f'{self.message if self.message else self.http_status.description}'

    def __repr__(self):
        return str(self)
