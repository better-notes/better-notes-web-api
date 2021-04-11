from fastapi import APIRouter
from fastapi.param_functions import Cookie

from web_api.accounts.dependencies import ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
from web_api.accounts.usecases import AccountSessionInteractor
from web_api.accounts.values import AuthenticationTokenValue
from web_api.commons.dependencies import PAGING_DEPENDENCY
from web_api.commons.values import Paging
from web_api.notes import entities, usecases, values
from web_api.notes.dependencies import NOTE_INTERACTOR_DEPENDENCY

router = APIRouter()


@router.post('/note/create/', response_model=list[entities.NoteEntity])
async def create_notes(
    note_values: list[values.NoteValue],
    authentication_token: str = Cookie(...),
    note_interactor: usecases.NoteInteractor = NOTE_INTERACTOR_DEPENDENCY,
    account_session_interactor: AccountSessionInteractor = (
        ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
    ),
) -> list[entities.NoteEntity]:
    """Add notes into db. Return added notes."""
    authentication_token_value = AuthenticationTokenValue(
        value=authentication_token,
    )
    account_session_entity = await account_session_interactor.get(
        authentication_token_value=authentication_token_value,
    )
    return await note_interactor.add(
        account_entity=account_session_entity.account,
        note_value_list=note_values,
    )


@router.get('/note/read/', response_model=list[entities.NoteEntity])
async def read_notes(
    paging: Paging = PAGING_DEPENDENCY,
    note_interactor: usecases.NoteInteractor = NOTE_INTERACTOR_DEPENDENCY,
    authentication_token: str = Cookie(...),
    account_session_interactor: AccountSessionInteractor = (
        ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
    ),
) -> list[entities.NoteEntity]:
    """Get all notes from db."""
    # TODO: add filtration by id or something
    authentication_token_value = AuthenticationTokenValue(
        value=authentication_token,
    )
    account_session_entity = await account_session_interactor.get(
        authentication_token_value=authentication_token_value,
    )
    return await note_interactor.get(
        account_entity=account_session_entity.account, paging=paging,
    )


@router.put('/note/update/', response_model=list[entities.NoteEntity])
async def update_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: usecases.NoteInteractor = NOTE_INTERACTOR_DEPENDENCY,
    authentication_token: str = Cookie(...),
    account_session_interactor: AccountSessionInteractor = (
        ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
    ),
) -> list[entities.NoteEntity]:
    """Update notes using id. Return updated notes."""
    authentication_token_value = AuthenticationTokenValue(
        value=authentication_token,
    )
    account_session_entity = await account_session_interactor.get(
        authentication_token_value=authentication_token_value,
    )
    return await note_interactor.update(
        account_entity=account_session_entity.account,
        note_entity_list=note_entities,
    )


@router.post('/note/delete/', response_model=list[entities.NoteEntity])
async def delete_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: usecases.NoteInteractor = NOTE_INTERACTOR_DEPENDENCY,
    authentication_token: str = Cookie(...),
    account_session_interactor: AccountSessionInteractor = (
        ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
    ),
) -> list[entities.NoteEntity]:
    """Delete notes using id. Return deleted notes."""
    authentication_token_value = AuthenticationTokenValue(
        value=authentication_token,
    )
    account_session_entity = await account_session_interactor.get(
        authentication_token_value=authentication_token_value,
    )
    return await note_interactor.delete(
        account_entity=account_session_entity.account,
        note_entity_list=note_entities,
    )
