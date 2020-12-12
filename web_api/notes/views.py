from web_api.notes.dependencies import get_note_interactor

from fastapi.param_functions import Depends
from web_api.notes import interactors
from web_api.notes import values, entities
from fastapi import APIRouter


router = APIRouter()


@router.post('/api/v1/note/create/', response_model=list[entities.NoteEntity])
async def create_notes(
    note_values: list[values.NoteValue],
    note_interactor: interactors.NoteInteractor = Depends(get_note_interactor),
) -> list[entities.NoteEntity]:
    return await note_interactor.add(note_values)


@router.get('/api/v1/note/read/', response_model=list[entities.NoteEntity])
async def read_notes(
    limit: int,
    offset: int,
    note_interactor: interactors.NoteInteractor = Depends(get_note_interactor),
) -> list[entities.NoteEntity]:
    # TODO: add limit & offset
    # TODO: add filtration by id or something
    return await note_interactor.get()


@router.put('/api/v1/note/update/', response_model=list[entities.NoteEntity])
async def update_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: interactors.NoteInteractor = Depends(get_note_interactor),
) -> list[entities.NoteEntity]:
    return await note_interactor.update(note_entities)


@router.post('/api/v1/note/delete/', response_model=list[entities.NoteEntity])
async def delete_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: interactors.NoteInteractor = Depends(get_note_interactor),
) -> list[entities.NoteEntity]:
    return await note_interactor.delete(note_entities)
