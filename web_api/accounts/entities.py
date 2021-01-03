from datetime import datetime
from web_api.accounts import values
from web_api.commons import entities


class UserEntity(entities.Entity):
    id_: str
    username: str
    password_hash: str
    created_at: datetime


class UserSessionEntity(entities.Entity):
    token: values.AuthenticationToken
    user: UserEntity
