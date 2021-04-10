from abc import ABC, abstractmethod

__all__ = ['ImageBase']


class ImageBase(ABC):
    @abstractmethod
    def save(self, image_data: bytes, folder: str = None, id: int = None) -> str:
        """
        :param image_data: bytes picture to save
        :param folder: folder for placing images
        :param id: image id
        :return: image url
        :raises ValueError: if invalid `image_data`
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, url: str) -> None:
        """
        :param url: url of the image to delete
        """
        raise NotImplementedError
