import dataclasses
from datetime import datetime, timezone

import bson
from motor import motor_asyncio
from pymongo.results import InsertOneResult
from web_api import commons
from web_api.commons.repositories import AbstractRepository
from web_api.notes import entities, values
from web_api.settings import Settings


@dataclasses.dataclass
class NoteRepository(AbstractRepository):
    client: motor_asyncio.AsyncIOMotorClient
    settings: Settings

    def __post_init__(self) -> None:
        db = self.client[self.settings.MONGO_DATABASE]
        self.notes_collection = db['notes']

    async def add(
        self, *, values: list[values.NoteValue]
    ) -> list[entities.NoteEntity]:
        inserted_entities = []

        for value in values:
            value_data = value.dict()
            created_at = datetime.now(timezone.utc)
            note_insert: InsertOneResult = (
                await self.notes_collection.insert_one(
                    {**value_data, 'created_at': created_at}
                )
            )
            inserted_entities.append(
                entities.NoteEntity(
                    id_=str(note_insert.inserted_id),
                    created_at=created_at,
                    **value_data,
                )
            )

        return inserted_entities

    async def get(
        self, *, spec: commons.specs.Specification, paging,
    ) -> list[entities.NoteEntity]:
        result = self.notes_collection.find(spec)
        raw_note_list = result.limit(paging.limit).skip(paging.offset)
        note_list = []
        async for note in raw_note_list:
            note_list.append(
                entities.NoteEntity(id_=str(note.pop('_id')), **note),
            )
        return note_list

    async def update(
        self, *, entities: list[entities.NoteEntity]
    ) -> list[entities.NoteEntity]:
        for entity in entities:
            entity_data = entity.dict(exclude={'id_'})
            await self.notes_collection.update_one(
                {'_id': bson.ObjectId(entity.id_)}, {'$set': entity_data},
            )
        return entities

    async def delete(
        self, *, entities: list[entities.NoteEntity]
    ) -> list[entities.NoteEntity]:
        id_value_list = []
        for entity in entities:
            id_value_list.append(bson.ObjectId(entity.id_))

        await self.notes_collection.delete_many(
            {'_id': {'$in': id_value_list}},
        )
        return entities
