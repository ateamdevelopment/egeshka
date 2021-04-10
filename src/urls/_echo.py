from typing import Final, final

from src.urls.base_urls import IpSessionUrl

__all__ = ['Echo']


@final
class Echo(IpSessionUrl):
    url: Final[str] = '/echo'

    def get(self, request_json):
        return request_json

    def post(self, request_json):
        return request_json

    def put(self, request_json):
        return request_json

    def delete(self, request_json):
        return request_json
