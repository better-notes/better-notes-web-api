from aiohttp import web

from web_api.notes import interactors, values, entities
from web_api import commons

routes = web.RouteTableDef()


@routes.view('/api/v1/note/create/', name='create_note')
class CreateNoteView(commons.views.StorableEntityView[values.NoteValue]):
    interactor: interactors.NoteInteractor = interactors.NoteInteractor()
    value_class = values.NoteValue

    async def post(self) -> web.Response:
        value_list = await self.get_values()
        entity_list = await self.interactor.add(value_list)
        entity_data = list(map(entities.NoteEntity.as_dict, entity_list))
        return commons.responses.MSGPackResponse(data=entity_data)


@routes.view('/api/v1/note/read/', name='read_note')
class ReadNoteView(commons.views.StorableEntityView[values.NoteValue]):
    interactor: interactors.NoteInteractor = interactors.NoteInteractor()
    value_class = values.NoteValue

    async def get(self) -> web.Response:
        entity_list = await self.interactor.get()
        entity_data = list(map(entities.NoteEntity.as_dict, entity_list))
        return commons.responses.MSGPackResponse(data=entity_data)


# TODO: Test.
@routes.view('/api/v1/note/update/', name='update_note')
class UpdateNoteView(commons.views.StorableEntityView[entities.NoteEntity]):
    interactor: interactors.NoteInteractor = interactors.NoteInteractor()
    value_class = entities.NoteEntity

    async def put(self) -> web.Response:
        value_list = await self.get_values()
        entity_list = await self.interactor.update(value_list)
        entity_data = list(map(entities.NoteEntity.as_dict, entity_list))
        return commons.responses.MSGPackResponse(data=entity_data)


@routes.view('/api/v1/note/delete/', name='delete_note')
class DeleteNoteView(commons.views.StorableEntityView[entities.NoteEntity]):
    interactor: interactors.NoteInteractor = interactors.NoteInteractor()
    value_class = entities.NoteEntity

    async def delete(self) -> web.Response:
        value_list = await self.get_values()
        entity_list = await self.interactor.delete(value_list)
        entity_data = list(map(entities.NoteEntity.as_dict, entity_list))
        return commons.responses.MSGPackResponse(data=entity_data)
