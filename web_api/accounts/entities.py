from datetime import datetime

from web_api.accounts import values
from web_api.commons import entities


class AccountEntity(entities.Entity):
    id_: str
    username: str
    password_hash: str
    created_at: datetime


class AccountSessionEntity(entities.Entity):
    token: values.AuthenticationTokenValue
    user: AccountEntity
