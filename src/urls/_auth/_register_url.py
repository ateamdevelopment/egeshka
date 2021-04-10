import re
from http import HTTPStatus
from typing import Final, final

from peewee import DoesNotExist

from src.models import User
from src.urls._auth._check_email_url import CheckEmailUrl
from src.urls.base_urls import IpSessionUrl
from src.urls.exceptions import HTTPException
from src.utils import email as util_email

__all__ = ['RegisterUrl']

_MAIL_REGEX: Final[re.Pattern] = re.compile(
    '^[a-zA-Z0-9]+([-._][a-zA-Z0-9]+)*@'
    '[a-zA-Z0-9]+([-.][a-zA-Z0-9]+)*\\.[a-zA-Z]{2,7}$'
)
_PASSWORD_REGEX: Final[re.Pattern] = re.compile('^[a-zA-Z0-9_]{6,}$')
_DEFAULT_MESSAGE: Final[str] = 'code: %s'  # TODO: read message from file


def _check_email_valid(email: str) -> bool:
    return bool(re.fullmatch(_MAIL_REGEX, email))


def _check_password_valid(password: str) -> bool:
    return bool(re.fullmatch(_PASSWORD_REGEX, password))


def _check_unique_email(email: str) -> bool:
    try:
        return User.get_by_email(email) is None
    except DoesNotExist:
        return True


def _send_code(email: str, code: int) -> None:
    util_email.send(
        message=_DEFAULT_MESSAGE % code,
        to=email
    )


@final
class RegisterUrl(IpSessionUrl):
    url: Final[str] = '/auth/register'

    def __init__(self, app):
        super().__init__(app)
        self.__last_code: int = 999  # start code == 1000

    @property
    def _code(self) -> int:
        if self.__last_code == 9999:
            self.__last_code = 999
        self.__last_code += 1
        return self.__last_code

    def post(self, request_json):
        email = self.get_value(request_json, 'email')
        password = self.get_value(request_json, 'password')

        if not _check_email_valid(email):
            raise HTTPException(HTTPStatus.BAD_REQUEST, '`email` is not valid')
        if not _check_password_valid(password):
            raise HTTPException(HTTPStatus.BAD_REQUEST, '`password` is not valid')

        if not _check_unique_email(email):
            return {'error': 1}

        code = self._code
        try:
            _send_code(email, code)
        except Exception:  # TODO: to clarify
            return {'error': 2}

        email_token = CheckEmailUrl.add_email(email, password, code)
        return {
            'email_token': email_token
        }
