import pytest
from aiohttp import web
from motor import motor_asyncio

from web_api import commons
from web_api.notes import interactors, repositories, views
from web_api.notes.tests import factories


class TestCreateNoteView:
    @pytest.fixture
    def note_data(self):
        return commons.msgpack.dumps([factories.NoteValueFactory().as_dict()])

    @pytest.fixture
    def view_cls(
        self, motor_client: motor_asyncio.AsyncIOMotorClient,
    ):
        class CreateNoteView(views.CreateNoteView):
            interactor: interactors.NoteInteractor = (
                interactors.NoteInteractor(
                    note_repository=repositories.NoteRepository(
                        client=motor_client
                    )
                )
            )

        return CreateNoteView

    async def test_post(
        self, view_cls, note_data, snapshot, aiohttp_client,
    ) -> None:
        # Given
        app = web.Application()
        app.router.add_view('/', view_cls)
        client = await aiohttp_client(app)
        # When
        res = await client.post('/', data=note_data)
        # Then
        content = await res.content.read()
        snapshot.assert_match(commons.msgpack.loads(content))


class TestReadNoteView:
    @pytest.fixture  # type: ignore
    def note_data(self):
        return commons.msgpack.dumps([factories.NoteValueFactory().as_dict()])

    @pytest.fixture  # type: ignore
    def view_cls(
        self, motor_client: motor_asyncio.AsyncIOMotorClient,
    ):
        class ReadNoteView(views.ReadNoteView):
            interactor: interactors.NoteInteractor = (
                interactors.NoteInteractor(
                    note_repository=repositories.NoteRepository(
                        client=motor_client
                    )
                )
            )

        return ReadNoteView

    async def test_post(
        self, aiohttp_client, view_cls, note_data, snapshot, motor_client,
    ) -> None:
        # Given
        app = web.Application()
        app.router.add_view('/', view_cls)
        client = await aiohttp_client(app)
        # And
        await interactors.NoteInteractor(
            repositories.NoteRepository(client=motor_client)
        ).add(factories.NoteValueFactory.create_batch(3))
        # When
        res = await client.get('/', data=note_data)
        # Then
        content = await res.content.read()
        snapshot.assert_match(commons.msgpack.loads(content))
