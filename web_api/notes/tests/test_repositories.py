from fastapi.encoders import jsonable_encoder
from syrupy.filters import props

from web_api.accounts.entities import AccountSessionEntity
from web_api.accounts.tests.factories.repository_factories import (
    AccountRepositoryFactory,
)
from web_api.accounts.tests.factories.value_factories import (
    AccountValueFactory,
)
from web_api.notes.tests import factories


class TestNoteRepository:
    async def get_account_entity(self) -> AccountSessionEntity:
        account_value = AccountValueFactory()
        account_repository = AccountRepositoryFactory()

        account_entities = await account_repository.add(
            account_value_list=[account_value],
        )

        return account_entities[0]

    async def test_add(self, snapshot) -> None:
        # Given
        account_entity = await self.get_account_entity()
        note = factories.NoteValueFactory()
        repository = factories.NoteRepositoryFactory()
        # When
        note_list = await repository.add(
            account_entity=account_entity, note_value_list=[note],
        )
        # Then
        assert jsonable_encoder(note_list) == snapshot(
            exclude=props('id_', 'created_at'),
        )
