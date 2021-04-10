"""
Util functions, classes and objects
"""
from typing import Final

from src import (
    DATABASE_URL,
    EMAIL_LOGIN, EMAIL_PASSWORD,
    CLOUDNARY_NAME, CLOUDNARY_KEY, CLOUDNARY_SECRET,
    YANDEX_DISK_TOKEN
)
from src.utils._cloudnary import Cloudnary
from src.utils._postgresql import PostgreSql
from src.utils._smtp_email import SmtpEmail
from src.utils._yandex_disk import YandexDisk
from src.utils.interfaces import Database, Email, ImageBase, FileBase

__all__ = ['email', 'database', 'image_base', 'file_base']

email: Final[Email] = SmtpEmail(EMAIL_LOGIN, EMAIL_PASSWORD)
database: Final[Database] = PostgreSql(DATABASE_URL)
image_base: Final[ImageBase] = Cloudnary(
    cloud_name=CLOUDNARY_NAME,
    api_key=CLOUDNARY_KEY,
    api_secret=CLOUDNARY_SECRET
)
file_base: Final[FileBase] = YandexDisk(YANDEX_DISK_TOKEN)
