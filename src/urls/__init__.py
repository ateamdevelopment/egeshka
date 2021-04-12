from flask import Flask

from src.urls._echo import Echo
# noinspection PyProtectedMember
from src.urls.auth import LogInUrl, CheckEmailUrl, RegisterUrl
# noinspection PyProtectedMember
from src.urls.user_urls import UserUrl, AvatarUrl

__all__ = ['init_urls']


def init_urls(app: Flask):
    RegisterUrl(app)
    LogInUrl(app)
    UserUrl(app)
    AvatarUrl(app)
    CheckEmailUrl(app)
    Echo(app)
