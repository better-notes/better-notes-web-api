import dataclasses

from typing import List
from web_api.notes import entities, repositories, values


@dataclasses.dataclass
class NoteInteractor:
    note_repository: repositories.NoteRepository = (
        repositories.NoteRepository()
    )

    async def add(self, values: List[values.Note]) -> List[entities.Note]:
        added_value = []
        for value in values:
            added_value.append(await self.note_repository.add(value))
        return added_value
