from __future__ import annotations

from typing import Callable

__all__ = ['Error']


class _ErrorMember:
    def __init__(self, code: int):
        self.code = code


class _ErrorMeta(type(Exception)):
    def __init__(self: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for member_name, member in args[2].items():
            if isinstance(member, _ErrorMember):
                setattr(self, member_name, self(member.code))


class Error(Exception, metaclass=_ErrorMeta):
    NO_SESSION: Error = _ErrorMember(100)

    def __init__(self, code):
        super().__init__()
        self.code = code

    def dict(self):
        return {'error': self.code}

    def __str__(self):
        return str(self.dict())
