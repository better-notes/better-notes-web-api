import dataclasses

from typing import List
from web_api.notes import entities, repositories, values, specs


def interactor_factory():
    return repositories.NoteRepository()


@dataclasses.dataclass
class NoteInteractor:
    note_repository: repositories.NoteRepository = dataclasses.field(
        default_factory=interactor_factory,
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
