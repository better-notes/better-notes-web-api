from fastapi.encoders import jsonable_encoder
from syrupy.filters import props

from web_api.notes import interactors
from web_api.notes.tests import factories


class TestNoteAPI:
    @property
    def interactor(self) -> interactors.NoteInteractor:
        return factories.NoteInteractorFactory()

    async def test_create(self, client, reverse_route, snapshot):
        note = factories.NoteValueFactory()

        response = await client.post(
            reverse_route('create_notes'), json=[note.dict()],
        )
        note_dict_list = response.json()

        assert note_dict_list == snapshot(exclude=props('created_at', 'id_'))

    async def test_read(self, client, reverse_route, snapshot):
        await self.interactor.add(
            note_value_list=[factories.NoteValueFactory()],
        )

        response = await client.get(
            '{0}{1}'.format(reverse_route('read_notes'), '?limit=10&offset=0'),
        )
        note_dict_list = response.json()

        assert note_dict_list == snapshot(exclude=props('created_at', 'id_'))

    async def test_update(self, client, reverse_route, snapshot):
        notes = await self.interactor.add(
            note_value_list=[factories.NoteValueFactory()],
        )
        note = notes[0]
        note.text = 'Updated note text'
        response = await client.put(
            reverse_route('update_notes'), json=jsonable_encoder([note]),
        )
        note_dict_list = response.json()

        assert note_dict_list == snapshot(exclude=props('created_at', 'id_'))

    async def test_delete(self, client, reverse_route, snapshot):
        notes = await self.interactor.add(
            note_value_list=[factories.NoteValueFactory()],
        )

        response = await client.post(
            reverse_route('delete_notes'), json=jsonable_encoder(notes),
        )
        note_dict_list = response.json()

        assert note_dict_list == snapshot(exclude=props('created_at', 'id_'))
