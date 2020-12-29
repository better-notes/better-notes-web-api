import dataclasses

from fastapi import HTTPException, status
from web_api.commons import values
from web_api.settings import Settings


@dataclasses.dataclass
class PagingTooWideException(HTTPException):
    settings: Settings
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def detail(self) -> str:
        return (
            'Given paging is too wide. '
            f'{self.settings.MAX_PAGING_LIMIT} is allowed.'
        )


@dataclasses.dataclass
class PagingValidator:
    """Validate that given paging doesn't exceed maximum paging limit."""

    settings: Settings

    def validate(self, *, paging: values.Paging) -> None:
        if paging.limit > self.settings.MAX_PAGING_LIMIT:
            raise PagingTooWideException(settings=self.settings)
