import dataclasses
from datetime import datetime, timedelta, timezone

import bson
from aioredis.commands import Redis
from motor import motor_asyncio
from pymongo.results import InsertOneResult
from web_api import commons
from web_api.accounts import entities, values
from web_api.commons.repositories import AbstractRepository
from web_api.settings import Settings


@dataclasses.dataclass
class UserRepository(AbstractRepository):
    client: motor_asyncio.AsyncIOMotorClient
    settings: Settings

    def __post_init__(self) -> None:
        db = self.client[self.settings.MONGO_DATABASE]
        self.users_collection = db['users']

    async def add(
        self, values: list[values.UserValue]
    ) -> list[entities.AccountEntity]:
        inserted_entities = []

        for value in values:
            value_data = value.dict()

            created_at = datetime.now(timezone.utc)
            user_insert: InsertOneResult = (
                await self.users_collection.insert_one(
                    {**value_data, 'created_at': created_at}
                )
            )

            inserted_entities.append(
                entities.AccountEntity(
                    id_=str(user_insert.inserted_id),
                    created_at=created_at,
                    **value_data,
                )
            )

        return inserted_entities

    async def get(
        self, *, spec: commons.specs.Specification, paging,
    ) -> list[entities.AccountEntity]:
        result = self.users_collection.find(spec)
        raw_user_list = result.limit(paging.limit).skip(paging.offset)
        user_list = []
        async for user in raw_user_list:
            user_list.append(
                entities.AccountEntity(id_=str(user.pop('_id')), **user),
            )
        return user_list

    async def update(
        self, *, entities: list[entities.AccountEntity]
    ) -> list[entities.AccountEntity]:
        for entity in entities:
            entity_data = entity.dict(exclude={'id_'})
            await self.users_collection.update_one(
                {'_id': bson.ObjectId(entity.id_)}, {'$set': entity_data},
            )
        return entities

    async def delete(
        self, *, entities: list[entities.AccountEntity]
    ) -> list[entities.AccountEntity]:
        id_value_list = []
        for entity in entities:
            id_value_list.append(bson.ObjectId(entity.id_))

        await self.users_collection.delete_many(
            {'_id': {'$in': id_value_list}},
        )
        return entities


@dataclasses.dataclass
class UserSessionRepository(AbstractRepository):
    client: Redis

    async def add(
        self, *, entities: list[entities.AccountSessionEntity]
    ) -> list[entities.AccountSessionEntity]:
        for entity in entities:
            await self.client.set(
                entity.token.value,
                entity.json(),
                expire=timedelta(days=7).seconds,
            )

        return entities

    async def get(
        self, *, values: list[values.AuthenticationTokenValue]
    ) -> list[entities.AccountSessionEntity]:
        result = []

        for value in values:
            entity_json = await self.client.get(value.value)
            result.append(entities.AccountSessionEntity.parse_raw(entity_json))

        return result
