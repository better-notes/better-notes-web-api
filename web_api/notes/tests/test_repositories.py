from fastapi.encoders import jsonable_encoder
from syrupy.filters import props

from web_api.notes.tests import factories


class TestNoteRepository:
    async def test_add(self, snapshot) -> None:
        # Given
        note = factories.NoteValueFactory()
        repository = factories.NoteRepositoryFactory()
        # When
        note_list = await repository.add(values=[note])
        # Then
        assert jsonable_encoder(note_list) == snapshot(
            exclude=props('id_', 'created_at'),
        )
