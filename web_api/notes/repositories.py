import abc
import dataclasses
from datetime import datetime, timezone
from typing import Any, List

from motor import motor_asyncio

from web_api import commons, settings
from web_api.notes import entities, values


class AbstractNoteRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, note: values.NoteValue) -> entities.NoteEntity:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(
        self, spec: commons.specs.Specification
    ) -> List[entities.NoteEntity]:
        raise NotImplementedError


@dataclasses.dataclass
class NoteRepository(AbstractNoteRepository):
    client: motor_asyncio.AsyncIOMotorClient = (
        motor_asyncio.AsyncIOMotorClient(
            settings.MONGO_HOST, settings.MONGO_PORT,
        )
    )

    def __post_init__(self) -> None:
        db = self.client[settings.MONGO_DATABASE]
        self.notes_collection = db['notes']
        self.tags_collection = db['tags']

    async def add_tags(
        self, tags: List[values.TagValue]
    ) -> List[entities.TagEntity]:
        added_tags = []
        for tag in tags:
            tag_data = tag.as_dict()
            created_at = datetime.now(timezone.utc)

            added_tag = await self.tags_collection.find_one_and_update(
                {'name': tag.name},
                {
                    '$setOnInsert': {
                        **tag_data.copy(),
                        **{'created_at': created_at},
                    }
                },
                upsert=True,
                return_document=True,
            )
            added_tags.append(
                entities.TagEntity(
                    id_=commons.values.ID(added_tag['_id']),
                    created_at=created_at,
                    **tag_data,
                )
            )
        return added_tags

    async def add(self, note: values.NoteValue) -> entities.NoteEntity:
        # TODO: add validation for already stored notes
        value_data = note.as_dict()
        created_at = datetime.now(timezone.utc)

        tags = await self.add_tags(note.tags)
        value_data['tags'] = list(map(values.TagValue.as_dict, tags))

        mongo_tag: Any = await self.notes_collection.insert_one(
            {**value_data.copy(), **{'created_at': created_at}}
        )
        return entities.NoteEntity(
            id_=commons.values.ID(mongo_tag.inserted_id),
            created_at=created_at,
            **value_data,
        )

    async def get(
        self, spec: commons.specs.Specification
    ) -> List[entities.NoteEntity]:
        result = self.notes_collection.find(spec.get_query())
        raw_note_list = await result.to_list(
            settings.REPOSITORY_DEFAULT_PAGE_SIZE
        )
        note_list = []
        for note in raw_note_list:
            note_list.append(
                entities.NoteEntity(
                    id_=commons.values.ID(note.pop('_id')), **note
                )
            )
        return note_list

    async def update(
        self, entities: List[entities.NoteEntity]
    ) -> List[entities.NoteEntity]:
        for entity in entities:
            entity_data = entity.as_dict()
            entity_data.pop('tags')
            entity_data.pop('id_')
            await self.notes_collection.update_one(
                {'_id': entity.id_.value}, {'$set': entity_data},
            )
        return entities

    async def delete(
        self, entities: List[entities.NoteEntity]
    ) -> List[entities.NoteEntity]:
        id_value_list = []
        for entity in entities:
            id_value_list.append(entity.id_.value)
        await self.notes_collection.delete_many(
            {'_id': {'$in': id_value_list}},
        )
        return entities
