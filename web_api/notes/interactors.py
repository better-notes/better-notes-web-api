import dataclasses
from web_api.commons.values import Paging

from web_api.notes import entities, repositories, values, specs


@dataclasses.dataclass
class NoteInteractor:
    note_repository: repositories.NoteRepository

    async def add(
        self, *, values: list[values.NoteValue]
    ) -> list[entities.NoteEntity]:
        return await self.note_repository.add(values=values)

    async def get(self, *, paging: Paging) -> list[entities.NoteEntity]:
        return await self.note_repository.get(
            spec=specs.ListNoteSpecification(), paging=paging,
        )

    async def update(
        self, *, entities: list[entities.NoteEntity]
    ) -> list[entities.NoteEntity]:
        return await self.note_repository.update(entities=entities)

    async def delete(
        self, *, entities: list[entities.NoteEntity]
    ) -> list[entities.NoteEntity]:
        return await self.note_repository.delete(entities=entities)
