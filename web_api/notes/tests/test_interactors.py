from fastapi.encoders import jsonable_encoder
from syrupy.filters import props

from web_api.accounts.entities import AccountEntity
from web_api.accounts.tests.factories.repository_factories import (
    AccountRepositoryFactory,
)
from web_api.accounts.tests.factories.value_factories import (
    AccountValueFactory,
)
from web_api.notes.tests import factories


class TestNoteInteractor:
    async def get_account_entity(self) -> AccountEntity:
        account_value = AccountValueFactory()
        account_repository = AccountRepositoryFactory()

        account_entities = await account_repository.add(
            account_value_list=[account_value],
        )

        return account_entities[0]

    async def test_add_get(self, snapshot) -> None:
        # Given
        account_entity = await self.get_account_entity()
        note_list = factories.NoteValueFactory.create_batch(3)
        # And
        interactor = factories.NoteInteractorFactory()
        # When
        await interactor.add(
            account_entity=account_entity, note_value_list=note_list,
        )
        note_entity_list = await interactor.get(
            account_entity=account_entity,
            paging=factories.PagingFactory(),
            ordering=factories.NoteOrderingFactory(),
        )
        # Then
        assert jsonable_encoder(note_entity_list) == snapshot(
            exclude=props('id_', 'created_at'),
        )

    async def test_update(self) -> None:
        # Given
        account_entity = await self.get_account_entity()
        interactor = factories.NoteInteractorFactory()
        note_list = factories.NoteValueFactory.create_batch(3)
        entity_list = await interactor.add(
            account_entity=account_entity, note_value_list=note_list,
        )
        # When
        entity_list[0].text = 'New text'
        await interactor.update(
            account_entity=account_entity, note_entity_list=entity_list,
        )
        entity_list = await interactor.get(
            account_entity=account_entity,
            paging=factories.PagingFactory(),
            ordering=factories.NoteOrderingFactory(),
        )
        # Then
        assert entity_list[0].text == 'New text'

    async def test_delete(self) -> None:
        # Given
        interactor = factories.NoteInteractorFactory()
        # And
        account_entity = await self.get_account_entity()
        note_list = factories.NoteValueFactory.create_batch(3)
        entity_list = await interactor.add(
            account_entity=account_entity, note_value_list=note_list,
        )
        # Ensure:
        note_entity_list = await interactor.get(
            account_entity=account_entity,
            paging=factories.PagingFactory(),
            ordering=factories.NoteOrderingFactory(),
        )
        assert note_entity_list != []

        # When
        await interactor.delete(
            account_entity=account_entity, note_entity_list=entity_list,
        )
        # Then
        note_entity_list = await interactor.get(
            account_entity=account_entity,
            paging=factories.PagingFactory(),
            ordering=factories.NoteOrderingFactory(),
        )
        assert note_entity_list == []
