from web_api.commons.values import Paging
from web_api.notes.dependencies import get_note_interactor

from fastapi.param_functions import Depends
from web_api.notes import interactors
from web_api.notes import values, entities
from fastapi import APIRouter


router = APIRouter()


@router.post('/note/create/', response_model=list[entities.NoteEntity])
async def create_notes(
    note_values: list[values.NoteValue],
    note_interactor: interactors.NoteInteractor = Depends(get_note_interactor),
) -> list[entities.NoteEntity]:
    return await note_interactor.add(values=note_values)


@router.get('/note/read/', response_model=list[entities.NoteEntity])
async def read_notes(
    paging: Paging = Depends(),
    note_interactor: interactors.NoteInteractor = Depends(get_note_interactor),
) -> list[entities.NoteEntity]:
    # TODO: add filtration by id or something
    return await note_interactor.get(paging=paging)


@router.put('/note/update/', response_model=list[entities.NoteEntity])
async def update_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: interactors.NoteInteractor = Depends(get_note_interactor),
) -> list[entities.NoteEntity]:
    return await note_interactor.update(entities=note_entities)


@router.post('/note/delete/', response_model=list[entities.NoteEntity])
async def delete_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: interactors.NoteInteractor = Depends(get_note_interactor),
) -> list[entities.NoteEntity]:
    return await note_interactor.delete(entities=note_entities)
