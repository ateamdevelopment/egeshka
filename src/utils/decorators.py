from logging import exception
from typing import Callable, TypeVar

__all__ = ['check_raises']

_TypeReturn = TypeVar('_TypeReturn')


def check_raises(function: Callable[..., _TypeReturn]) -> Callable[..., _TypeReturn]:
    def check(*args, **kwargs):
        # noinspection PyBroadException
        try:
            return function(*args, **kwargs)
        except Exception as e:
            # noinspection PyUnresolvedReferences
            exception(
                f'''(
    {function.__module__ = },
    {function.__name__ = }
): {{
    {args = },
    {kwargs = }
}}'''
            )
            raise e

    return check
