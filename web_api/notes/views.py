import dataclasses

from aiohttp import web

from web_api.notes import interactors, values
from web_api import commons

routes = web.RouteTableDef()


@routes.view('/', name='create_note')
class CreateNoteView(commons.views.StorableEntityView):
    interactor: interactors.NoteInteractor = interactors.NoteInteractor()
    value_class = values.Note

    async def post(self) -> web.Response:
        value = await self.get_value()
        entity = await self.interactor.add(value)
        entity_data = dataclasses.asdict(entity)
        return commons.responses.MSGPackResponse(data=entity_data)
