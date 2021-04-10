from abc import ABC, abstractmethod
from typing import BinaryIO

__all__ = ['FileBase']


class FileBase(ABC):
    @abstractmethod
    def upload(self, file: BinaryIO, path: str) -> None:
        """
        :param file: uploaded file is opened in 'rb' mode
        :param path: destination path
        :raise FileExistsError: if file on the base already exists
        """
        raise NotImplementedError
