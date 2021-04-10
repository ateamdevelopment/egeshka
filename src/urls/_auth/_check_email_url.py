from __future__ import annotations

from http import HTTPStatus
from logging import warning
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
            del cls.__email_sessions[session.token]
            del cls.__cache_email_sessions[email]
            del cls.__cache_code_sessions[session.code]
        except KeyError:
            pass

    @classmethod
    def __generate_token(cls) -> str:
        return generate_random_token(cls.LENGTH_TOKEN)

    @classmethod
    def __get_session(cls, token: str) -> __EmailSession:
        try:
            return cls.__email_sessions[token]
        except KeyError:
            warning(f'Not email token ({token})')
            raise HTTPException(HTTPStatus.UNAUTHORIZED, f'Not valid {cls.NAME_TOKEN}')

    def post(self, request_json):
        token = self.get_value(request_json, self.NAME_TOKEN)
        code = self.get_value(request_json, 'code', int)
        if code == (session := self.__get_session(token)).code:
            user = User.create(session.email, session.password)
            self.__delete_session(session.email)
            user_token = UserSessionUrl.add_user_session(user)
            return {
                'user_token': user_token
            }
        return {
            'error': 1
        }
