from http import HTTPStatus
from typing import final

from src.urls.exceptions import HTTP_Exception

__all__ = ['NoParameterException']


@final
class NoParameterException(HTTP_Exception):
    def __init__(self, name_parameter: str):
        super().__init__(
            HTTPStatus.BAD_REQUEST,
            f'No required parameter `{name_parameter}`'
        )
