import dataclasses

import bson

from web_api.accounts.entities import AccountEntity
from web_api.commons.specs import merge_specs
from web_api.commons.values import Paging
from web_api.notes import specs
from web_api.notes.entities import NoteEntity
from web_api.notes.repositories import NoteRepository
from web_api.notes.values import NoteOrdering, NoteValue, TagValue


@dataclasses.dataclass
class NoteInteractor:
    """Interactor for notes."""

    note_repository: NoteRepository

    async def add(
        self, *, account_entity: AccountEntity, note_value_list: list[NoteValue],
    ) -> list[NoteEntity]:
        """Add notes into db. Return added notes."""
        return await self.note_repository.add(
            account_entity=account_entity, note_value_list=note_value_list,
        )

    async def get(
        self,
        *,
        account_entity: AccountEntity,
        paging: Paging,
        ordering: NoteOrdering,
        tag_value_list: list[TagValue],
    ) -> list[NoteEntity]:
        """Return all notes."""
        if tag_value_list:
            spec = merge_specs(
                specs.GetNoteSpecification(username=account_entity.username),
                specs.GetNoteByTagsSpecification(tag_value_list=tag_value_list),
            )
        else:
            spec = specs.GetNoteSpecification(username=account_entity.username)

        return await self.note_repository.get(spec=spec, paging=paging, ordering=ordering)

    async def update(
        self, *, account_entity: AccountEntity, note_entity_list: list[NoteEntity],
    ) -> list[NoteEntity]:
        """Update given notes using id. Return updated notes."""
        for note_entity in note_entity_list:
            await self.note_repository.update(
                spec=specs.UpdateNoteSpecification(
                    username=account_entity.username, _id=bson.ObjectId(note_entity.id_),
                ),
                note_value=NoteValue(**note_entity.dict(exclude={'id_', 'created_at', 'account'})),
            )

        return note_entity_list

    async def delete(
        self, *, account_entity: AccountEntity, note_entity_list: list[NoteEntity],
    ) -> list[NoteEntity]:
        """Delete given notes using id. Return delete notes."""
        object_id_list = []
        for note_entity in note_entity_list:
            object_id_list.append(bson.ObjectId(note_entity.id_))

        await self.note_repository.delete(
            spec=specs.DeleteNoteSpecification(
                username=account_entity.username, object_id_list=object_id_list,
            ),
        )

        return note_entity_list
