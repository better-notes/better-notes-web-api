import dataclasses

from aiohttp import web

from web_api.notes import interactors, values
from web_api import commons

routes = web.RouteTableDef()


@routes.view('/api/v1/note/create/', name='create_note')
class CreateNoteView(commons.views.StorableEntityView):
    interactor: interactors.NoteInteractor = interactors.NoteInteractor()
    value_class = values.Note

    async def post(self) -> web.Response:
        values = await self.get_values()
        entities = await self.interactor.add(values)
        entities_data = list(map(dataclasses.asdict, entities))
        return commons.responses.MSGPackResponse(data=entities_data)
