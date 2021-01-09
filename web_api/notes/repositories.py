import dataclasses
from datetime import datetime, timezone

from motor import motor_asyncio
from pymongo.results import InsertOneResult

from web_api.accounts.entities import AccountEntity
from web_api.commons.repositories import AbstractRepository
from web_api.commons.values import Paging
from web_api.notes import entities, values
from web_api.notes.specs import NoteSpecification
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
        self,
        *,
        account_entity: AccountEntity,
        note_value_list: list[values.NoteValue],
    ) -> list[entities.NoteEntity]:
        """Add notes into db. Return added notes."""
        inserted_entities = []

        for note_value in note_value_list:
            note_value_dict = note_value.dict()
            created_at = datetime.now(timezone.utc)
            note_insert: InsertOneResult = (
                await self.notes_collection.insert_one(
                    {
                        'account': account_entity.dict(),
                        **note_value_dict,
                        'created_at': created_at,
                    },
                )
            )
            inserted_entities.append(
                entities.NoteEntity(
                    id_=str(note_insert.inserted_id),
                    account=account_entity,
                    **note_value_dict,
                    created_at=created_at,
                ),
            )

        return inserted_entities

    async def get(
        self, *, spec: NoteSpecification, paging: Paging,
    ) -> list[entities.NoteEntity]:
        """Return notes for given spec."""
        cursor = self.notes_collection.find(spec.get_query())

        raw_note_list = cursor.limit(paging.limit).skip(paging.offset)
        note_list = []
        async for note in raw_note_list:
            note_list.append(
                entities.NoteEntity(id_=str(note.pop('_id')), **note),
            )
        return note_list

    async def update(
        self, *, spec: NoteSpecification, note_value: values.NoteValue,
    ) -> int:
        """Update notes using spec. Return updated amount."""
        note_value_dict = note_value.dict()

        update_result = await self.notes_collection.update_one(
            spec.get_query(), {'$set': note_value_dict},
        )
        return update_result.modified_count

    async def delete(self, *, spec: NoteSpecification) -> int:
        """Delete notes using spec. Return deleted amount."""
        delete_result = await self.notes_collection.delete_many(
            spec.get_query(),
        )
        return delete_result.deleted_count
