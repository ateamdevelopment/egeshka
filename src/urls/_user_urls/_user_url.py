from typing import Final, final

from src.urls.base_urls import UserSessionUrl
from src.utils import image_base

__all__ = ['UserUrl']


@final
class UserUrl(UserSessionUrl):
    url: Final[str] = '/user'

    def _get(self, request_json, session):
        return session.user.serialize()

    def _delete(self, request_json, session):
        user = session.user
        if avatar_url := user.avatar_url:
            image_base.delete(avatar_url)
        user.delete_instance(recursive=True)
        UserSessionUrl.delete_user_session(user)
        return {}
