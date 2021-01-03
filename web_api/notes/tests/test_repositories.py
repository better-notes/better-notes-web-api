from fastapi.encoders import jsonable_encoder
from syrupy.filters import props
from web_api.notes.tests import factories


class TestNoteRepository:
    async def test_add(self, snapshot) -> None:
        # Given
        note = factories.NoteValueFactory()
        repository = factories.NoteRepositoryFactory()
        # When
        result = await repository.add(values=[note])
        # Then
        assert jsonable_encoder(result) == snapshot(
            exclude=props('id_', 'created_at'),
        )
