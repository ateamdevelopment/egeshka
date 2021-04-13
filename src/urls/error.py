from __future__ import annotations

from typing import Final, TypedDict

__all__ = ['TypeError_', 'Error']


class TypeError_(TypedDict):
    error: int


class _ErrorMember:
    def __init__(self, code: int):
        self.code: Final[int] = code


class _ErrorMeta(type):
    def __init__(cls, *args, **kwargs):
        type.__init__(cls, *args, **kwargs)
        for member_name, member in args[2].items():
            if isinstance(member, _ErrorMember):
                setattr(cls, member_name, cls(member.code))


class Error(dict, metaclass=_ErrorMeta):
    NO_SESSION: TypeError_ = _ErrorMember(100)

    def __init__(self, code):
        super().__init__(error=code)
