import dataclasses
from datetime import datetime, timedelta, timezone

import bson
from aioredis.commands import Redis
from fastapi import HTTPException, status
from motor import motor_asyncio
from pymongo.errors import DuplicateKeyError
from pymongo.results import InsertOneResult

from web_api import commons
from web_api.accounts import entities, values
from web_api.commons.repositories import AbstractRepository
from web_api.settings import Settings


@dataclasses.dataclass
class AccountDuplicateUsernameError(HTTPException):
    """Raised when trying to create account w/ already existing username."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = 'Account with given username already exist.'


@dataclasses.dataclass
class AccountRepository(AbstractRepository):
    """Repository for accounts."""

    client: motor_asyncio.AsyncIOMotorClient
    settings: Settings

    @property
    def db(self) -> motor_asyncio.AsyncIOMotorDatabase:
        """Mongo database instance."""
        return self.client[self.settings.mongo_database]

    @property
    def users_collection(self) -> motor_asyncio.AsyncIOMotorCollection:
        """Accounts collection instalce."""
        return self.db[self.settings.accounts_collection]

    async def add(
        self, *, account_value_list: list[values.AccountValue],
    ) -> list[entities.AccountEntity]:
        inserted_entities = []

        for account_value in account_value_list:
            value_data = account_value.dict()

            created_at = datetime.now(timezone.utc)
            try:
                user_insert: InsertOneResult = (
                    await self.users_collection.insert_one(
                        {**value_data, 'created_at': created_at},
                    )
                )
            except DuplicateKeyError:
                raise AccountDuplicateUsernameError()

            value_data.pop('password_hash')
            inserted_entities.append(
                entities.AccountEntity(
                    id_=str(user_insert.inserted_id),
                    created_at=created_at,
                    **value_data,
                ),
            )

        return inserted_entities

    async def get(
        self,
        *,
        spec: commons.specs.Specification,
        paging: commons.values.Paging,
    ) -> list[entities.AccountEntity]:
        # fmt: off
        cursor = self.users_collection.find(
            spec.get_query(),
        ).limit(paging.limit).skip(paging.offset)
        # fmt: on

        account_entity_list = []
        async for account_entity_dict in cursor:
            account_entity_dict.pop('password_hash')
            account_entity_list.append(
                entities.AccountEntity(
                    id_=str(account_entity_dict.pop('_id')),
                    **account_entity_dict,
                ),
            )
        return account_entity_list

    async def update(
        self, *, account_entity_list: list[entities.AccountEntity],
    ) -> list[entities.AccountEntity]:
        for entity in account_entity_list:
            entity_data = entity.dict(exclude={'id_'})
            await self.users_collection.update_one(
                {'_id': bson.ObjectId(entity.id_)}, {'$set': entity_data},
            )
        return account_entity_list

    async def delete(
        self, *, account_entity_list: list[entities.AccountEntity],
    ) -> list[entities.AccountEntity]:
        id_value_list = []
        for entity in account_entity_list:
            id_value_list.append(bson.ObjectId(entity.id_))

        await self.users_collection.delete_many(
            {'_id': {'$in': id_value_list}},
        )
        return account_entity_list

    async def get_password_hash(
        self, *, account_entity: entities.AccountEntity,
    ) -> str:
        """Get password hash for given account entity."""
        account_entity_projection = await self.users_collection.find_one(
            {'_id': bson.ObjectId(account_entity.id_)}, ['password_hash'],
        )
        return account_entity_projection['password_hash']


@dataclasses.dataclass
class AccountSessionNotFoundError(HTTPException):
    """Raised when account session with given id doesn't exist in store."""

    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = 'Account session with given id was not found.'


@dataclasses.dataclass
class AccountSessionRepository(AbstractRepository):
    """Repository for account sessions."""

    client: Redis

    async def add(
        self,
        *,
        account_session_entity_list: list[entities.AccountSessionEntity],
    ) -> list[entities.AccountSessionEntity]:
        for account_session_entity in account_session_entity_list:
            await self.client.set(
                account_session_entity.token.value,
                account_session_entity.json(),
                expire=timedelta(days=7).seconds,
            )

        return account_session_entity_list

    async def get(
        self,
        *,
        authentication_token_value_list: list[values.AuthenticationTokenValue],
    ) -> list[entities.AccountSessionEntity]:
        account_session_entity_list = []

        for authentication_token_value in authentication_token_value_list:
            entity_json = await self.client.get(
                authentication_token_value.value,
            )

            if entity_json is None:
                raise AccountSessionNotFoundError()

            account_session_entity_list.append(
                entities.AccountSessionEntity.parse_raw(entity_json),
            )

        return account_session_entity_list
