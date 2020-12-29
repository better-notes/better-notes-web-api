import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from syrupy.filters import props
from web_api.main import get_application
from web_api.notes import interactors
from web_api.notes.tests import factories


@pytest.fixture
def app():
    return get_application()


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture
def reverse_route(app):
    def _reverse_route(route_name, *args, **kwargs):
        return app.url_path_for(route_name, *args, **kwargs)

    return _reverse_route


class TestNoteAPI:
    @property
    def interactor(self) -> interactors.NoteInteractor:
        return factories.NoteInteractorFactory()

    async def test_create(self, client, reverse_route, snapshot):
        note = factories.NoteValueFactory()

        response = await client.post(
            reverse_route('create_notes'), json=[note.dict()]
        )
        data = response.json()

        assert data == snapshot(exclude=props('created_at', 'id_'))

    async def test_read(self, client, reverse_route, snapshot):
        await self.interactor.add(values=[factories.NoteValueFactory()])

        response = await client.get(
            reverse_route('read_notes') + '?limit=10&offset=0',
        )
        data = response.json()

        assert data == snapshot(exclude=props('created_at', 'id_'))

    async def test_update(self, client, reverse_route, snapshot):
        notes = await self.interactor.add(
            values=[factories.NoteValueFactory()]
        )
        note = notes[0]
        note.text = 'Updated note text'
        response = await client.put(
            reverse_route('update_notes'), json=jsonable_encoder([note]),
        )
        data = response.json()

        assert data == snapshot(exclude=props('created_at', 'id_'))

    async def test_delete(self, client, reverse_route, snapshot):
        notes = await self.interactor.add(
            values=[factories.NoteValueFactory()]
        )

        response = await client.post(
            reverse_route('delete_notes'), json=jsonable_encoder(notes),
        )
        data = response.json()

        assert data == snapshot(exclude=props('created_at', 'id_'))
