from fastapi.encoders import jsonable_encoder
from syrupy.filters import props
from web_api.notes.tests import factories


class TestNoteInteractor:
    async def test_add_get(self, snapshot) -> None:
        # Given
        note_list = factories.NoteValueFactory.create_batch(3)
        # And
        interactor = factories.NoteInteractorFactory()
        # When
        await interactor.add(note_list)
        result = await interactor.get()
        # Then
        assert jsonable_encoder(result) == snapshot(
            exclude=props('id_', 'created_at')
        )

    async def test_update(self) -> None:
        # Given
        interactor = factories.NoteInteractorFactory()
        note_list = factories.NoteValueFactory.create_batch(3)
        entity_list = await interactor.add(note_list)
        # When
        entity_list[0].text = 'New text'
        await interactor.update(entity_list)
        entity_list = await interactor.get()
        # Then
        assert entity_list[0].text == 'New text'

    async def test_delete(self) -> None:
        # Given
        interactor = factories.NoteInteractorFactory()
        # And
        note_list = factories.NoteValueFactory.create_batch(3)
        entity_list = await interactor.add(note_list)
        # Ensure:
        assert await interactor.get() != []

        # When
        await interactor.delete(entity_list)
        # Then
        assert await interactor.get() == []
