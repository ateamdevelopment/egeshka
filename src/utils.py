import os
from typing import Type, Any, TypeVar

from src import IS_HOST


def path_to_src():
    if IS_HOST:
        return os.getcwd() + '/src'
    return os.getcwd()


T = TypeVar("T")


class NoPublicConstructor(type):
    """
    Metaclass that ensures a private constructor

    If you try to instantiate your class (`SomeClass()`),
    a `TypeError` will be thrown.
    """

    def __call__(cls, *args, **kwargs):
        """
        :raises TypeError - always
        """
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )

    def _create(cls: Type[T], *args, **kwargs) -> T:
        return super().__call__(*args, **kwargs)
