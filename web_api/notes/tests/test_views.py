import dataclasses
from typing import Any, cast

import pytest
from aiohttp import test_utils, web
from motor import motor_asyncio

from web_api import commons
from web_api import main
from web_api.notes import entities, interactors, repositories, views
from web_api.notes.tests import factories


@pytest.fixture  # type: ignore
async def client(test_client: Any) -> test_utils.TestClient:
    return cast(test_utils.TestClient, await test_client(main.create_app))


class TestCreateNoteView:
    @pytest.fixture  # type: ignore
    def note_data(self) -> entities.Note:
        result: entities.Note = commons.msgpack.dumps(
            dataclasses.asdict(factories.NoteFactory())
        )
        return result

    @pytest.fixture  # type: ignore
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
        self,
        client: test_utils.TestClient,
        aiohttp_client,
        view_cls,
        note_data,
        snapshot,
    ) -> None:
        # Given
        # import ipdb; ipdb.set_trace()
        app = web.Application()
        app.router.add_view('/', view_cls)

        client = await aiohttp_client(app)
        res = await client.post('/', data=note_data)

        assert res.status == 200
        content = await res.content.read()
        snapshot.assert_match(commons.msgpack.loads(content))
