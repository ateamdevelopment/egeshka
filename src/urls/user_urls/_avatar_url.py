import base64
import binascii
from http import HTTPStatus
from typing import Final, final

from src.urls.base_urls import UserSessionUrl
from src.urls.exceptions import HTTP_Exception
from src.utils import image_base

__all__ = ['AvatarUrl']


@final
class AvatarUrl(UserSessionUrl):
    url: Final[str] = '/user/avatar'

    def _put(self, request_json, session):
        try:
            avatar_data: bytes = base64.b64decode(
                self.get_value(request_json, 'avatar_data')
            )
        except binascii.Error:
            raise HTTP_Exception(
                HTTPStatus.BAD_REQUEST,
                '`avatar_data` encoding must be base64 (/+)'
            )
        try:
            avatar_url = image_base.save(avatar_data, folder='avatars')
        except ValueError:
            raise HTTP_Exception(
                HTTPStatus.BAD_REQUEST,
                'Invalid `avatar_data`'
            )
        user = session.user
        if old_avatar_url := user.avatar_url:
            image_base.delete(old_avatar_url)

        user.avatar_url = avatar_url
        user.save()
        return {'avatar_url': avatar_url}

    def _delete(self, request_json, session):
        user = session.user
        if avatar_url := user.avatar_url:
            image_base.delete(avatar_url)
        del user.avatar_url
        user.save()
        return {}
