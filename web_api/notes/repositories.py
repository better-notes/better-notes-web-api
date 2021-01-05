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
    """Repository for notes."""

    client: motor_asyncio.AsyncIOMotorClient
    settings: Settings

    def __post_init__(self) -> None:
        """Initialize mongo client."""
        db = self.client[self.settings.MONGO_DATABASE]
        self.notes_collection = db['notes']

    async def add(
        self, *, note_value_list: list[values.NoteValue],
    ) -> list[entities.NoteEntity]:
        """Add notes into db. Return added notes."""
        inserted_entities = []

        for note_value in note_value_list:
            note_value_dict = note_value.dict()
            created_at = datetime.now(timezone.utc)
            note_insert: InsertOneResult = (
                await self.notes_collection.insert_one(
                    {**note_value_dict, 'created_at': created_at},
                )
            )
            inserted_entities.append(
                entities.NoteEntity(
                    id_=str(note_insert.inserted_id),
                    created_at=created_at,
                    **note_value_dict,
                ),
            )

        return inserted_entities

    async def get(
        self, *, spec: commons.specs.Specification, paging,
    ) -> list[entities.NoteEntity]:
        """Return notes for given spec."""
        cursor = self.notes_collection.find(spec)

        raw_note_list = cursor.limit(paging.limit).skip(paging.offset)
        note_list = []
        async for note in raw_note_list:
            note_list.append(
                entities.NoteEntity(id_=str(note.pop('_id')), **note),
            )
        return note_list

    async def update(
        self, *, note_entity_list: list[entities.NoteEntity],
    ) -> list[entities.NoteEntity]:
        """Update notes using id. Return updated notes."""
        for note_entity in note_entity_list:
            note_entity_dict = note_entity.dict(exclude={'id_'})
            await self.notes_collection.update_one(
                {'_id': bson.ObjectId(note_entity.id_)},
                {'$set': note_entity_dict},
            )
        return note_entity_list

    async def delete(
        self, *, note_entity_list: list[entities.NoteEntity],
    ) -> list[entities.NoteEntity]:
        """Delete notes using id. Return delete notes."""
        id_value_list = []
        for note_entity in note_entity_list:
            id_value_list.append(bson.ObjectId(note_entity.id_))

        await self.notes_collection.delete_many(
            {'_id': {'$in': id_value_list}},
        )
        return note_entity_list
