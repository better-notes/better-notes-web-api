from syrupy.filters import props
from web_api.notes.tests import factories


class TestNoteRepository:
    async def test_add(self, snapshot) -> None:
        # Given
        note = factories.NoteValueFactory()
        repository = factories.NoteRepositoryFactory()
        # When
        result = await repository.add(note=note)
        # Then
        assert result.dict() == snapshot(exclude=props('id_', 'created_at'),)
