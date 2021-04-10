from __future__ import annotations

import os
import re
from tempfile import TemporaryFile
from logging import warning
from typing import Final, final

import cloudinary
from cloudinary.api import delete_resources
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from src.utils.decorators import check_raises
from src.utils.interfaces import ImageBase

# noinspection SpellCheckingInspection
__all__ = ['Cloudnary']


@check_raises
def _parse_url(image_url: str) -> tuple[str, str]:
    index = re.search('image/upload/(v\\d+/)?', image_url)
    if index is None:
        raise ValueError

    image_path = image_url[index.end():]
    if (index := re.search('/.+$', image_path)) is None:
        folder = None
        full_image_id = image_path
    else:
        index = index.start()
        folder = image_path[:index]
        full_image_id = image_path[index + 1:]

    try:
        index = full_image_id.index('.')
        image_id = full_image_id[:index]
    except ValueError:
        image_id = full_image_id

    return folder, image_id


# noinspection SpellCheckingInspection
@final
class Cloudnary(ImageBase):
    class Image:
        def __init__(self, image_url: str):
            folder, image_id = _parse_url(image_url)
            self.folder: Final[str] = folder
            self.image_id: Final[str] = image_id

        @property
        def id(self) -> str:
            if self.folder is None:
                return self.image_id
            return f'{self.folder}/{self.image_id}'

    def __init__(self, cloud_name: str, api_key: int, api_secret: str):
        """
        :raises cloudinary.exceptions.AuthorizationRequired: if not valid
            `cloud_name` or `api_key` or `api_secret`
        """
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        cloudinary.api.subfolders('/')  # check authorization

    @check_raises
    def save(self, image_data, folder=None, id=None):
        try:
            with TemporaryFile() as image:
                image.write(image_data)
                image.seek(0)
                image_id = upload(
                    file=image,
                    folder=folder,
                    public_id=id
                )['public_id']
        except cloudinary.exceptions.Error:
            raise ValueError
        return cloudinary_url(image_id)[0]

    @check_raises
    def delete(self, url):
        try:
            image = self.Image(url)
            delete_resources(image.id)
        except ValueError:
            warning(f'Couldn\'t parse url: {url}')
