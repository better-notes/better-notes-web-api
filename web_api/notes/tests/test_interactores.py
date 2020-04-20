import dataclasses

import pytest

from web_api.notes import interactors, repositories
from web_api.notes.tests import factories
from funcy import lmap


class TestNoteInteractor:
    @pytest.mark.asyncio
    async def test_add_get(self, motor_client, snapshot) -> None:
        # Given
        note_list = factories.NoteFactory.create_batch(3)
        # And
        interactor = interactors.NoteInteractor(
            repositories.NoteRepository(client=motor_client)
        )
        # When
        await interactor.add(note_list)
        result = await interactor.get()
        # Then
        snapshot.assert_match(lmap(dataclasses.asdict, result))
