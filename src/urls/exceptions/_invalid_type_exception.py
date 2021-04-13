from http import HTTPStatus
from typing import Type, final

from src.urls.exceptions._http_exception import HTTP_Exception

__all__ = ['InvalidTypeException']


@final
class InvalidTypeException(HTTP_Exception):
    def __init__(self, requirement_type: Type, name_parameter: str):
        super().__init__(
            HTTPStatus.BAD_REQUEST,
            f'`{name_parameter}` must be <{requirement_type.__name__}>'
        )
