import dataclasses

from web_api.notes import interactors, repositories
from web_api.notes.tests import factories
from funcy import lmap


class TestNoteInteractor:
    async def test_add_get(self, motor_client, snapshot) -> None:
        # Given
        note_list = factories.NoteValueFactory.create_batch(3)
        # And
        interactor = interactors.NoteInteractor(
            repositories.NoteRepository(client=motor_client)
        )
        # When
        await interactor.add(note_list)
        result = await interactor.get()
        # Then
        snapshot.assert_match(lmap(dataclasses.asdict, result))

    async def test_update(self, motor_client, snapshot) -> None:
        # Given
        interactor = interactors.NoteInteractor(
            repositories.NoteRepository(client=motor_client)
        )
        # And
        note_list = factories.NoteValueFactory.create_batch(3)
        entity_list = await interactor.add(note_list)
        # When
        await interactor.update(
            [dataclasses.replace(entity_list[0], text='New text')]
        )
        entity_list = await interactor.get()
        # Then
        assert entity_list[0].text == 'New text'
