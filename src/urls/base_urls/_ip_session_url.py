from __future__ import annotations

from abc import ABC
from datetime import datetime, timedelta
from http import HTTPStatus
from logging import warning
from typing import Final, Optional

from flask import Request

from src.urls.base_urls._base_url import BaseUrl
from src.urls.exceptions import HTTP_Exception

__all__ = ['IpSessionUrl']


def _get_ip(request: Request) -> Optional[str]:
    env = request.environ
    return env.get('HTTP_X_FORWARDED_FOR') or env.get('REMOTE_ADDR')


class IpSessionUrl(BaseUrl, ABC):
    """
    The URL that supports sessions by IP. To get an IP, a proxy is required
    """

    class __LocalSession:
        ban_count: int = 30
        ban_period: float = 10
        ban_time: float = 60

        def __init__(self, ip: str):
            self.ip: Final[str] = ip
            self.__time_requests: set[datetime] = set()
            self.__time_last_ban: Optional[datetime] = None

        def mark(self) -> None:
            self.__time_requests.add(datetime.now())

        def is_ban(self) -> bool:
            """
            :return: True - if session is banned, False - if else
            """
            now = datetime.now()
            if self.__time_last_ban is not None:
                if (now - self.__time_last_ban) < timedelta(seconds=self.ban_time):
                    return True
                self.__time_last_ban = None

            delta = timedelta(seconds=self.ban_period)
            self.__time_requests = set(
                time_request for time_request in self.__time_requests if
                (now - time_request) < delta
            )
            if len(self.__time_requests) >= self.ban_count:
                self.__time_last_ban = now
                return True
            return False

    class __GlobalSession(__LocalSession):
        ban_count: int = 150
        ban_period: float = 30
        ban_time: float = 3600  # 60 * 60 - 1 hour

    __global_ip_sessions: Final[dict[str, __GlobalSession]] = {}

    def __init__(self, app):
        super().__init__(app)
        self.__local_ip_session: Final[dict[str, IpSessionUrl.__LocalSession]] = {}

    def _get_request(self) -> Request:
        request = super()._get_request()
        if (ip := _get_ip(request)) is None:
            warning(f'No IP in request (\n\t{request.environ = }\n)')
            raise HTTP_Exception(HTTPStatus.UNAUTHORIZED, 'No IP')

        if (global_session := IpSessionUrl.__global_ip_sessions.get(ip)) is None:
            global_session = IpSessionUrl.__GlobalSession(ip)
            IpSessionUrl.__global_ip_sessions[ip] = global_session

        if (local_session := self.__local_ip_session.get(ip)) is None:
            local_session = self.__LocalSession(ip)
            self.__local_ip_session[ip] = local_session

        self.__check_session(global_session)
        self.__check_session(local_session)
        return request

    @staticmethod
    def __check_session(session: IpSessionUrl.__LocalSession) -> None:
        session.mark()
        if session.is_ban():
            warning(f'IP {session.ip} was banned')
            raise HTTP_Exception(HTTPStatus.FORBIDDEN, 'Exceeded the number of requests')
