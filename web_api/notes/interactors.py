import dataclasses

from typing import List
from web_api.notes import entities, repositories, values, specs


@dataclasses.dataclass
class NoteInteractor:
    note_repository: repositories.NoteRepository = (
        repositories.NoteRepository()
    )

    async def add(
        self, values: List[values.NoteValue]
    ) -> List[entities.NoteEntity]:
        added_value = []
        for value in values:
            added_value.append(await self.note_repository.add(value))
        return added_value

    async def get(self) -> List[entities.NoteEntity]:
        return await self.note_repository.get(specs.ListNoteSpecification())

    async def update(
        self, entities: List[entities.NoteEntity]
    ) -> List[entities.NoteEntity]:
        return await self.note_repository.update(entities)

    async def delete(
        self, entities: List[entities.NoteEntity]
    ) -> List[entities.NoteEntity]:
        return await self.note_repository.delete(entities)
