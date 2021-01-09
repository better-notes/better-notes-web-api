from datetime import datetime

from web_api.accounts.entities import AccountEntity
from web_api.commons import entities
from web_api.notes import values


class NoteEntity(entities.Entity):
    """Aggregate which represents note."""

    id_: str
    account: AccountEntity
    text: str
    tags: list[values.TagValue]
    created_at: datetime
