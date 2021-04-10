from typing import Union, Any

__all__ = ['TypePrimitives', 'TypeJson']

TypePrimitives = Union[int, str, float, bool, bytes]
TypeJson = dict[str, Union[TypePrimitives, dict[str, Any], None]]
