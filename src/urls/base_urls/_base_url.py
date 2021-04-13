import json
from abc import ABC, abstractmethod
from http import HTTPStatus
from logging import exception, info, warning
from typing import Final, Type, TypeVar

from flask import Flask, Request, Response, request as flask_request

from src.urls.exceptions import (
    Error, HTTP_Exception, InvalidTypeException, NoParameterException
)
from src.utils.types import TypeJson

__all__ = ['BaseUrl']

_RequirementType = TypeVar('_RequirementType')


class BaseUrl(ABC):
    def __init__(self, app: Flask):
        self.app: Final[Flask] = app

        try:
            app.add_url_rule(
                rule=self.url,
                endpoint=self.__class__.__name__,
                view_func=self._index,
                methods=['GET', 'POST', 'PUT', 'DELETE']
            )
        except AssertionError:
            exception(f'{self.__class__.__name__}: repeat call __init__')
            raise

        info(f'{self.__class__.__name__} ({self.url}) inited')

    def _index(self) -> Response:
        response: Request
        # noinspection PyBroadException
        try:
            request = self._get_request()
            info(f'{self.__class__.__name__}: request = {request.__dict__}')
            request_json = self._parse_request(request)
            info(f'{self.__class__.__name__}: {request_json = }')

            method = request.method.upper()
            if method == 'GET':
                response_json = self.get(request_json)
            elif method == 'POST':
                response_json = self.post(request_json)
            elif method == 'PUT':
                response_json = self.put(request_json)
            elif method == 'DELETE':
                response_json = self.delete(request_json)
            else:
                warning(f'{self.__class__.__name__}: method {method} not allowed')
                raise HTTP_Exception(HTTPStatus.METHOD_NOT_ALLOWED)

            info(f'{self.__class__.__name__}: {response_json = }')
            response = self._make_response(response_json)
        except Error as error:
            warning(f'{self.__class__.__name__}: {error = }')
            response = self._make_error_response(error)
        except HTTP_Exception as http_exception:
            warning(f'{self.__class__.__name__}: {http_exception = }')
            response = self._make_exception_response(http_exception)
        except Exception:
            exception(f'{self.__class__.__name__}')
            response = self._make_exception_response()
        return response

    def _get_request(self) -> Request:
        return flask_request

    @staticmethod
    def _parse_request(request: Request) -> TypeJson:
        """
        :param request: current http request
        :return: JSON parsed from request.data or request.form | request.args
        :raises HTTPException: if decoding to utf-8 or deserializing to JSON failed
        """
        try:
            if request.data:
                return json.loads(request.data.decode('utf-8'))
            return request.form | request.args
        except UnicodeDecodeError:
            raise HTTP_Exception(HTTPStatus.BAD_REQUEST, 'The encoding must be UTF-8')
        except json.JSONDecodeError:
            raise HTTP_Exception(HTTPStatus.BAD_REQUEST, 'Bad JSON')

    def _make_response(self, response_json: TypeJson) -> Response:
        """
        :param response_json: server response in JSON format
        :return: server's final response
        """
        return self.app.make_response(json.dumps(response_json))

    def _make_error_response(self, error: Error) -> Response:
        return self.app.make_response(error.dict())

    def _make_exception_response(
            self,
            http_exception: HTTP_Exception = HTTP_Exception()
    ) -> Response:
        """
        :param http_exception: the exception that occurred.
            Default: INTERNAL_SERVER_ERROR (500)
        :return: server's final response to the error
        """
        response: Response = self.app.make_response(str(http_exception))
        response.status_code = http_exception.http_status.value
        return response

    @property
    @abstractmethod
    def url(self) -> str:
        """
        :return: rule starting with '/'
        """
        raise NotImplementedError

    def get(self, request_json: TypeJson) -> TypeJson:
        """
        :param request_json: current http request in JSON format
        :return: GET method response
        """
        raise HTTP_Exception(HTTPStatus.METHOD_NOT_ALLOWED)

    def post(self, request_json: TypeJson) -> TypeJson:
        """
        :param request_json: current http request in JSON format
        :return: POST method response
        """
        raise HTTP_Exception(HTTPStatus.METHOD_NOT_ALLOWED)

    def put(self, request_json: TypeJson) -> TypeJson:
        """
        :param request_json: current http request in JSON format
        :return: PUT method response
        """
        raise HTTP_Exception(HTTPStatus.METHOD_NOT_ALLOWED)

    def delete(self, request_json: TypeJson) -> TypeJson:
        """
        :param request_json: current http request in JSON format
        :return: DELETE method response
        """
        raise HTTP_Exception(HTTPStatus.METHOD_NOT_ALLOWED)

    @staticmethod
    def get_value(
            request_json: TypeJson,
            name_parameter: str,
            requirement_type: Type[_RequirementType] = str
    ) -> _RequirementType:
        f"""
        :return: a required parameter in the `request_json`
        :raises NoParameterException: if {name_parameter} key not in `request_json`
        :raises InvalidTypeException: if {name_parameter} not casted to {requirement_type}
        """
        # noinspection PyBroadException
        try:
            return requirement_type(request_json[name_parameter])
        except KeyError:
            raise NoParameterException(name_parameter)
        except (ValueError, TypeError):
            raise InvalidTypeException(requirement_type, name_parameter)
        except Exception:
            warning(
                f'''
Unusual exception when trying to cast {name_parameter} to {requirement_type.__name__}
{{
    {requirement_type = }
    parameter = {request_json.get(name_parameter)}
}}
'''
            )
            raise InvalidTypeException(requirement_type, name_parameter)
