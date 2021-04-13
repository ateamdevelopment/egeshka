from typing import Final, final

from peewee import DoesNotExist

from src.models import User
from src.urls.exceptions import Error
from src.urls.base_urls import IpSessionUrl, UserSessionUrl

__all__ = ['LogInUrl']


@final
class LogInUrl(IpSessionUrl):
    url: Final[str] = '/auth/log_in'

    NotExistsUserError: Final[Error] = Error(1)
    MismatchedPasswordError: Final[Error] = Error(2)

    def get(self, request_json):
        email = self.get_value(request_json, 'email')
        password = self.get_value(request_json, 'password')

        try:
            user = User.get_by_email(email)
        except DoesNotExist:
            raise self.NotExistsUserError
        if user.password != password:
            raise self.MismatchedPasswordError
        user_token = UserSessionUrl.add_user_session(user)
        return {'user_token': user_token}
