from http import HTTPStatus
from typing import final

from src.urls.exceptions import HTTPException

__all__ = ['NoParameterException']


@final
class NoParameterException(HTTPException):
    def __init__(self, name_parameter: str):
        super().__init__(
            HTTPStatus.BAD_REQUEST,
            f'No required parameter `{name_parameter}`'
        )
