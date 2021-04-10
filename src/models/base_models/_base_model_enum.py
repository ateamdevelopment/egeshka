from src.models.base_models._base_model import BaseModel

__all__ = ['BaseModelEnum']


class _ModelEnumMeta(type(BaseModel), type):
    def __init__(cls, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        cls._init_static()

    def _init_static(cls) -> None:
        pass


class BaseModelEnum(BaseModel, metaclass=_ModelEnumMeta):
    def delete_instance(self, recursive=False, delete_nullable=False):
        """
        :raises AttributeError: if call
        """
        raise AttributeError("Enum elements cannot be deleted")
