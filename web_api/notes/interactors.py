import dataclasses

from web_api.notes import entities, repositories, values, specs


@dataclasses.dataclass
class NoteInteractor:
    note_repository: repositories.NoteRepository

    async def add(
        self, values: list[values.NoteValue]
    ) -> list[entities.NoteEntity]:
        added_value = []
        for value in values:
            added_value.append(await self.note_repository.add(value))
        return added_value

    async def get(self) -> list[entities.NoteEntity]:
        return await self.note_repository.get(specs.ListNoteSpecification())

    async def update(
        self, entities: list[entities.NoteEntity]
    ) -> list[entities.NoteEntity]:
        return await self.note_repository.update(entities)

    async def delete(
        self, entities: list[entities.NoteEntity]
    ) -> list[entities.NoteEntity]:
        return await self.note_repository.delete(entities)
