from fastapi import APIRouter

from web_api.commons.dependencies import PAGING_DEPENDENCY
from web_api.commons.values import Paging
from web_api.notes import entities, interactors, values
from web_api.notes.dependencies import NOTE_INTERACTOR_DEPENDENCY

router = APIRouter()


@router.post('/note/create/', response_model=list[entities.NoteEntity])
async def create_notes(
    note_values: list[values.NoteValue],
    note_interactor: interactors.NoteInteractor = NOTE_INTERACTOR_DEPENDENCY,
) -> list[entities.NoteEntity]:
    """Add notes into db. Return added notes."""
    return await note_interactor.add(note_value_list=note_values)


@router.get('/note/read/', response_model=list[entities.NoteEntity])
async def read_notes(
    paging: Paging = PAGING_DEPENDENCY,
    note_interactor: interactors.NoteInteractor = NOTE_INTERACTOR_DEPENDENCY,
) -> list[entities.NoteEntity]:
    """Get all notes from db."""
    # TODO: add filtration by id or something
    return await note_interactor.get(paging=paging)


@router.put('/note/update/', response_model=list[entities.NoteEntity])
async def update_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: interactors.NoteInteractor = NOTE_INTERACTOR_DEPENDENCY,
) -> list[entities.NoteEntity]:
    """Update notes using id. Return updated notes."""
    return await note_interactor.update(note_entity_list=note_entities)


@router.post('/note/delete/', response_model=list[entities.NoteEntity])
async def delete_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: interactors.NoteInteractor = NOTE_INTERACTOR_DEPENDENCY,
) -> list[entities.NoteEntity]:
    """Delete notes using id. Return deleted notes."""
    return await note_interactor.delete(note_entity_list=note_entities)
