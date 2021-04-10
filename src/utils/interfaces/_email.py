from abc import ABC, abstractmethod

__all__ = ['Email']


class Email(ABC):
    @abstractmethod
    def send(self, message: str, to: str, subject: str = None) -> None:
        """
        :param message: the text of the e-mail
        :param to: to whom the e-mail is sent
        :param subject: the subject of the e-mail
        :raises TODO
        """
        raise NotImplementedError
