import dataclasses
from web_api.notes import values, entities, repositories


@dataclasses.dataclass
class NoteInteractor:
    note_repository: repositories.NoteRepository = (
        repositories.NoteRepository()
    )

    async def add(self, value: values.Note) -> entities.Note:
        return await self.note_repository.add(value)
