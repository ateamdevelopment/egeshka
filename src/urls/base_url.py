from typing import Any, final
from abc import ABC, ABCMeta, abstractmethod
from http import HTTPStatus
import json

from flask import (
    Flask,
    Response,
    Request,
    request as flask_request
)

from src.urls.exceptions import HTTPException

__all__ = ['BaseUrl']


class _MetaBaseUrl(ABCMeta):
    __classes = set()

    @property
    def classes(cls) -> frozenset:
        return frozenset(cls.__classes)

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if ABC not in cls.__bases__:
            mcs.__classes.add(cls)
        return cls


class BaseUrl(ABC, metaclass=_MetaBaseUrl):
    def __init__(self, app: Flask):
        self.__app = app

        def index() -> Response:
            response: Request
            # noinspection PyBroadException
            try:
                request_json = self._parse_request(flask_request)
                response_json = self.reply(request_json)
                response = self._make_response(response_json)
            except HTTPException as http_exception:
                response = self._make_error_response(http_exception)
            except Exception:
                response = self._make_error_response()
            return response

        try:
            app.add_url_rule(
                rule=self.url,
                endpoint=self.__class__.__name__,
                view_func=index,
                methods=self.methods
            )
        except AssertionError:
            # TODO: logging - repeat call __init__
            pass

    @staticmethod
    def _parse_request(request: Request) -> dict[str, Any]:
        try:
            if request.data:
                return json.loads(request.data.decode('utf-8'))
            return request.form or request.args
        except UnicodeDecodeError:
            raise HTTPException(HTTPStatus.BAD_REQUEST, 'The encoding must be UTF-8')
        except json.JSONDecodeError:
            raise HTTPException(HTTPStatus.BAD_REQUEST, 'Bad json')

    def _make_response(self, response_json: dict[str, Any]) -> Response:
        return self.__app.make_response(json.dumps(response_json))

    def _make_error_response(
            self,
            http_exception: HTTPException = HTTPException()
    ) -> Response:
        response: Response = self.__app.make_response(str(http_exception))
        response.status_code = http_exception.http_status.value
        return response

    @property
    @final
    def app(self) -> Flask:
        return self.__app

    @property
    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def methods(self) -> list[str]:
        """
        :return: list of literals GET, POST, PUT, DELETE
        """
        raise NotImplementedError

    @abstractmethod
    def reply(self, request: dict[str, Any]) -> dict[str, Any]:
        """
        :param request: received request in JSON format
        :return: response to the request in JSON format
        :raises HTTPException: if there are errors
        """
        raise NotImplementedError
