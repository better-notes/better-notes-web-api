import dataclasses

from web_api.commons.values import Paging
from web_api.notes import specs
from web_api.notes.entities import NoteEntity
from web_api.notes.repositories import NoteRepository
from web_api.notes.values import NoteValue


@dataclasses.dataclass
class NoteInteractor:
    """Interactor for notes."""

    note_repository: NoteRepository

    async def add(
        self, *, note_value_list: list[NoteValue],
    ) -> list[NoteEntity]:
        """Add notes into db. Return added notes."""
        return await self.note_repository.add(note_value_list=note_value_list)

    async def get(self, *, paging: Paging) -> list[NoteEntity]:
        """Return all notes."""
        return await self.note_repository.get(
            spec=specs.NoteSpecification(), paging=paging,
        )

    async def update(
        self, *, note_entity_list: list[NoteEntity],
    ) -> list[NoteEntity]:
        """Update given notes using id. Return updated notes."""
        return await self.note_repository.update(
            note_entity_list=note_entity_list,
        )

    async def delete(
        self, *, note_entity_list: list[NoteEntity],
    ) -> list[NoteEntity]:
        """Delete given notes using id. Return delete notes."""
        return await self.note_repository.delete(
            note_entity_list=note_entity_list,
        )
