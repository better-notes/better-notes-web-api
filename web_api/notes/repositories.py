import abc
import dataclasses
from datetime import datetime, timezone
from typing import Any, List

from motor import motor_asyncio

from web_api import commons, settings
from web_api.notes import entities, values


class AbstractNoteRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, note: values.Note) -> entities.Note:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, spec: commons.specs.Specification) -> entities.Note:
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

    async def add_tags(self, tags: List[values.Tag]) -> List[entities.Tag]:
        added_tags = []
        for tag in tags:
            tag_data = dataclasses.asdict(tag)
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
                entities.Tag(
                    id_=commons.values.ID(added_tag['_id']),
                    created_at=created_at,
                    **tag_data,
                )
            )
        return added_tags

    async def add(self, note: values.Note) -> entities.Note:
        # TODO: add validation for already stored notes
        value_data = dataclasses.asdict(note)
        created_at = datetime.now(timezone.utc)

        tags = await self.add_tags(note.tags)
        value_data['tags'] = list(map(dataclasses.asdict, tags))

        mongo_tag: Any = await self.notes_collection.insert_one(
            {**value_data.copy(), **{'created_at': created_at}}
        )
        return entities.Note(
            id_=commons.values.ID(mongo_tag.inserted_id),
            created_at=created_at,
            **value_data,
        )

    async def get(self, spec: commons.specs.Specification) -> entities.Note:
        raise NotImplementedError
