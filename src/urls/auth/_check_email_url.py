from __future__ import annotations

from http import HTTPStatus
from logging import warning, debug
from typing import Final, final

from src.models import User
from src.urls.base_urls import IpSessionUrl, UserSessionUrl
from src.urls.exceptions import HTTPException
from src.utils.functions import generate_random_token

__all__ = ['CheckEmailUrl']


@final
class CheckEmailUrl(IpSessionUrl):
    class __EmailSession:
        def __init__(self, token: str, email: str, password: str, code: int):
            self.token: Final[str] = token
            self.email: Final[str] = email
            self.password: Final[str] = password
            self.code: Final[int] = code

    url: Final[str] = '/auth/check_email'

    LENGTH_TOKEN: Final[int] = 30
    NAME_TOKEN: Final[str] = 'email_token'

    __email_sessions: Final[dict[str, __EmailSession]] = {}
    __cache_email_sessions: Final[dict[str, __EmailSession]] = {}
    __cache_code_sessions: Final[dict[int, __EmailSession]] = {}

    @classmethod
    def add_email(cls, email: str, password: str, code: int) -> str:
        if (session := cls.__cache_code_sessions.get(code)) is not None:
            if email == session.email:
                return session.token
            cls.__delete_session(session.email)

        token = cls.__generate_token()
        while token in cls.__email_sessions:
            token = cls.__generate_token()

        session = cls.__EmailSession(token, email, password, code)
        cls.__email_sessions[token] = session
        cls.__cache_email_sessions[email] = session
        cls.__cache_code_sessions[code] = session
        return token

    @classmethod
    def __delete_session(cls, email: str) -> None:
        try:
            session = cls.__cache_email_sessions[email]
        except KeyError:
            warning(
                f'No session for such key ({email = })'
                f'in sessions ({cls.__cache_email_sessions = })'
            )
            return
        try:
            del cls.__email_sessions[session.token]
            del cls.__cache_email_sessions[email]
            del cls.__cache_code_sessions[session.code]
        except KeyError:
            warning(
                f'Cache error:\n'
                f'{session.token = } -> {cls.__email_sessions = }\n'
                f'{email = } -> {cls.__cache_email_sessions = }\n'
                f'{session.code = } -> {cls.__cache_code_sessions = }'
            )

    @classmethod
    def __generate_token(cls) -> str:
        return generate_random_token(cls.LENGTH_TOKEN)

    @classmethod
    def __get_session(cls, token: str) -> __EmailSession:
        try:
            return cls.__email_sessions[token]
        except KeyError as key_error:
            warning(
                f'No email session for this token ({token})'
                f'in sessions ({cls.__email_sessions = })'
            )
            raise key_error

    def post(self, request_json):
        token = self.get_value(request_json, self.NAME_TOKEN)
        code = self.get_value(request_json, 'code', int)
        try:
            session = self.__get_session(token)
        except KeyError:
            return {'error': 100}
        if code == session.code:
            user = User.create(session.email, session.password)
            self.__delete_session(session.email)
            user_token = UserSessionUrl.add_user_session(user)
            return {
                'user_token': user_token
            }
        return {
            'error': 1
        }
