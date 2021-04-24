from fastapi import APIRouter, Depends

from web_api.accounts.dependencies.requests import (
    get_authentication_token_value,
)
from web_api.accounts.dependencies.usecases import (
    get_account_session_interactor,
)
from web_api.accounts.usecases import AccountSessionInteractor
from web_api.accounts.values import AuthenticationTokenValue
from web_api.commons.dependencies import get_paging
from web_api.commons.values import Paging
from web_api.notes import entities, usecases, values
from web_api.notes.dependencies import get_note_interactor, get_tag_value_list

router = APIRouter()


@router.post('/note/create/', response_model=list[entities.NoteEntity])
async def create_notes(
    note_values: list[values.NoteValue],
    authentication_token_value: AuthenticationTokenValue = Depends(
        get_authentication_token_value,
    ),
    note_interactor: usecases.NoteInteractor = Depends(get_note_interactor),
    account_session_interactor: AccountSessionInteractor = Depends(
        get_account_session_interactor,
    ),
) -> list[entities.NoteEntity]:
    """Add notes into db. Return added notes."""
    account_session_entity = await account_session_interactor.get(
        authentication_token_value=authentication_token_value,
    )
    return await note_interactor.add(
        account_entity=account_session_entity.account,
        note_value_list=note_values,
    )


@router.get('/note/read/', response_model=list[entities.NoteEntity])
async def read_notes(  # noqa: WPS211 # Too many args.
    ordering: values.NoteOrdering = Depends(values.NoteOrdering),
    paging: Paging = Depends(get_paging),
    tag_value_list: list[values.TagValue] = Depends(get_tag_value_list),
    note_interactor: usecases.NoteInteractor = Depends(get_note_interactor),
    authentication_token_value: AuthenticationTokenValue = Depends(
        get_authentication_token_value,
    ),
    account_session_interactor: AccountSessionInteractor = Depends(
        get_account_session_interactor,
    ),
) -> list[entities.NoteEntity]:
    """Get all notes from db."""
    account_session_entity = await account_session_interactor.get(
        authentication_token_value=authentication_token_value,
    )
    return await note_interactor.get(
        account_entity=account_session_entity.account,
        paging=paging,
        ordering=ordering,
        tag_value_list=tag_value_list,
    )


@router.put('/note/update/', response_model=list[entities.NoteEntity])
async def update_notes(
    note_entities: list[entities.NoteEntity],
    note_interactor: usecases.NoteInteractor = Depends(get_note_interactor),
    authentication_token_value: AuthenticationTokenValue = Depends(
        get_authentication_token_value,
    ),
    account_session_interactor: AccountSessionInteractor = Depends(
        get_account_session_interactor,
    ),
) -> list[entities.NoteEntity]:
    """Update notes using id. Return updated notes."""
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
    note_interactor: usecases.NoteInteractor = Depends(get_note_interactor),
    authentication_token_value: AuthenticationTokenValue = Depends(
        get_authentication_token_value,
    ),
    account_session_interactor: AccountSessionInteractor = Depends(
        get_account_session_interactor,
    ),
) -> list[entities.NoteEntity]:
    """Delete notes using id. Return deleted notes."""
    account_session_entity = await account_session_interactor.get(
        authentication_token_value=authentication_token_value,
    )
    return await note_interactor.delete(
        account_entity=account_session_entity.account,
        note_entity_list=note_entities,
    )
