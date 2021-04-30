from typing import Union, Any, TypedDict

__all__ = ['TypePrimitives', 'TypeJson', 'UserInfo']

TypePrimitives = Union[int, str, float, bool, bytes]
TypeJson = dict[str, Union[TypePrimitives, dict[str, Any], None]]


class UserInfo(TypedDict):
    email: str
    password: str
    first_name: str
    last_name: str
