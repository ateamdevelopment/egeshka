from typing import Final, final

from yadisk import YaDisk
from yadisk.exceptions import PathExistsError

from src.utils.decorators import check_raises
from src.utils.interfaces import FileBase

__all__ = ['YandexDisk']


@final
class YandexDisk(FileBase):
    def __init__(self, token: str):
        self.ya_disk: Final[YaDisk] = YaDisk(
            token=token
        )
        if not self.ya_disk.check_token():
            raise ValueError('Yandex disk token is invalid')

    @check_raises
    def upload(self, file, path):
        try:
            self.ya_disk.upload(file, path)
        except PathExistsError:
            raise FileExistsError
