from typing import Final, final

from src.models import Subject
from src.urls.base_urls import IpSessionUrl

__all__ = ['SubjectUrl']


@final
class SubjectUrl(IpSessionUrl):
    url: Final[str] = '/subject'

    def get(self, request_json):
        id_ = self.get_value(request_json, 'id')
        subject = Subject.get_by_id(id_)
        return subject.serialize()
