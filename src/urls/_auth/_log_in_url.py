from typing import Final, final

from peewee import DoesNotExist

from src.models import User
from src.urls.base_urls import IpSessionUrl, UserSessionUrl

__all__ = ['LogInUrl']


@final
class LogInUrl(IpSessionUrl):
    url: Final[str] = '/auth/log_in'

    def get(self, request_json):
        email = self.get_value(request_json, 'email')
        password = self.get_value(request_json, 'password')

        try:
            user = User.get_by_email(email)
        except DoesNotExist:
            return {'error': 1}
        if user.password != password:
            return {'error': 2}
        user_token = UserSessionUrl.add_user_session(user)
        return {
            'user_token': user_token
        }
