from functools import lru_cache

from aiohttp import web

from web_api import commons
from web_api.notes import entities, interactors, values

routes = web.RouteTableDef()


@routes.view('/api/v1/note/create/', name='create_note')
class CreateNoteView(commons.views.StorableEntityView[values.NoteValue]):
    value_class = values.NoteValue

    @lru_cache()
    def get_interactor(self) -> interactors.NoteInteractor:
        return interactors.NoteInteractor()

    async def post(self) -> web.Response:
        value_list = await self.get_values()
        entity_list = await self.get_interactor().add(value_list)
        entity_data = list(map(entities.NoteEntity.as_dict, entity_list))
        return commons.responses.MSGPackResponse(data=entity_data)


@routes.view('/api/v1/note/read/', name='read_note')
class ReadNoteView(commons.views.StorableEntityView[values.NoteValue]):
    value_class = values.NoteValue

    @lru_cache()
    def get_interactor(self) -> interactors.NoteInteractor:
        return interactors.NoteInteractor()

    async def get(self) -> web.Response:
        entity_list = await self.get_interactor().get()
        entity_data = list(map(entities.NoteEntity.as_dict, entity_list))
        return commons.responses.MSGPackResponse(data=entity_data)


@routes.view('/api/v1/note/update/', name='update_note')
class UpdateNoteView(commons.views.StorableEntityView[entities.NoteEntity]):
    value_class = entities.NoteEntity

    @lru_cache()
    def get_interactor(self) -> interactors.NoteInteractor:
        return interactors.NoteInteractor()

    async def post(self) -> web.Response:
        value_list = await self.get_values()
        entity_list = await self.get_interactor().update(value_list)
        entity_data = list(map(entities.NoteEntity.as_dict, entity_list))
        return commons.responses.MSGPackResponse(data=entity_data)
