from fastapi.encoders import jsonable_encoder
from syrupy.filters import props

from web_api.accounts.entities import AccountSessionEntity
from web_api.accounts.repositories import AccountRepository
from web_api.accounts.tests.factories.repositories import AccountRepositoryFactory
from web_api.accounts.tests.factories.usecases import AccountSessionInteractorFactory
from web_api.accounts.tests.factories.values import AccountValueFactory
from web_api.accounts.values import AccountValue
from web_api.notes import usecases
from web_api.notes.tests import factories


class TestNoteAPI:
    @property
    def interactor(self) -> usecases.NoteInteractor:
        return factories.NoteInteractorFactory()

    async def get_account_session(self) -> AccountSessionEntity:
        account_value: AccountValue = AccountValueFactory()
        account_repository: AccountRepository = AccountRepositoryFactory()
        account_session_interactor = await AccountSessionInteractorFactory()

        account_entities = await account_repository.add(account_value_list=[account_value])
        return await account_session_interactor.add(account_entity=account_entities[0])

    async def test_create(self, client, reverse_route, snapshot):
        note = factories.NoteValueFactory()
        account_session_entity = await self.get_account_session()
        response = await client.post(
            reverse_route('create_notes'),
            json=[note.dict()],
            cookies={'authentication_token': account_session_entity.token.value},
        )
        note_dict_list = response.json()
        assert note_dict_list == snapshot(exclude=props('created_at', 'id_'))

    async def test_read(self, client, reverse_route, snapshot):
        account_session_entity = await self.get_account_session()
        await self.interactor.add(
            account_entity=account_session_entity.account,
            note_value_list=[factories.NoteValueFactory()],
        )

        response = await client.get(
            '{0}{1}'.format(
                reverse_route('read_notes'), '?limit=10&offset=0&created_at=ascending',
            ),
            cookies={'authentication_token': account_session_entity.token.value},
        )
        note_dict_list = response.json()

        assert note_dict_list == snapshot(exclude=props('created_at', 'id_'))

    async def test_update(self, client, reverse_route, snapshot):
        account_session_entity = await self.get_account_session()
        notes = await self.interactor.add(
            account_entity=account_session_entity.account,
            note_value_list=[factories.NoteValueFactory()],
        )
        note = notes[0]
        note.text = 'Updated note text'
        response = await client.put(
            reverse_route('update_notes'),
            json=jsonable_encoder([note]),
            cookies={'authentication_token': account_session_entity.token.value},
        )
        note_dict_list = response.json()

        assert note_dict_list == snapshot(exclude=props('created_at', 'id_'))

    async def test_delete(self, client, reverse_route, snapshot):
        account_session_entity = await self.get_account_session()
        notes = await self.interactor.add(
            account_entity=account_session_entity.account,
            note_value_list=[factories.NoteValueFactory()],
        )

        response = await client.post(
            reverse_route('delete_notes'),
            json=jsonable_encoder(notes),
            cookies={'authentication_token': account_session_entity.token.value},
        )
        note_dict_list = response.json()

        assert note_dict_list == snapshot(exclude=props('created_at', 'id_'))
