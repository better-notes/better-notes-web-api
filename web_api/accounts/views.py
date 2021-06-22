from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.responses import JSONResponse

from web_api.accounts.dependencies.requests import get_authentication_token_value
from web_api.accounts.dependencies.usecases import (
    get_account_authenticate_use_case,
    get_account_register_use_case,
    get_account_session_interactor,
)
from web_api.accounts.entities import AccountEntity
from web_api.accounts.usecases import (
    AccountAuthenticateUseCase,
    AccountRegisterUseCase,
    AccountSessionInteractor,
)
from web_api.accounts.values import (
    AuthenticationCredentialsValue,
    AuthenticationTokenValue,
    RegistrationCredentialsValue,
)
from web_api.notes.dependencies import get_add_welcome_note_usecase
from web_api.notes.usecases import AddWelcomeNoteUsecase

router = APIRouter()


@router.post('/account/register/')
async def register(
    registration_credentials: RegistrationCredentialsValue,
    account_register_use_case: AccountRegisterUseCase = Depends(get_account_register_use_case),
    add_welcome_note_usecase: AddWelcomeNoteUsecase = Depends(get_add_welcome_note_usecase),
) -> JSONResponse:
    account_session_entity = await account_register_use_case.register(
        registration_credentials=registration_credentials,
    )

    await add_welcome_note_usecase.add_welcome_note(account_entity=account_session_entity.account)

    response = JSONResponse(content={})
    response.set_cookie(
        key='authentication_token', value=account_session_entity.token.value, httponly=True,
    )

    return response


@router.post('/account/authenticate/')
async def authenticate(
    authentication_credentials: AuthenticationCredentialsValue,
    account_authenticate_use_case: AccountAuthenticateUseCase = Depends(
        get_account_authenticate_use_case,
    ),
) -> JSONResponse:
    account_session_entity = await account_authenticate_use_case.authenticate(
        authentication_credentials=authentication_credentials,
    )

    response = JSONResponse(content={})
    response.set_cookie(
        key='authentication_token', value=account_session_entity.token.value, httponly=True,
    )

    return response


@router.get('/account/profile/', response_model=AccountEntity)
async def profile(
    authentication_token_value: AuthenticationTokenValue = Depends(get_authentication_token_value),
    account_session_interactor: AccountSessionInteractor = Depends(get_account_session_interactor),
) -> AccountEntity:
    """Get current account data."""
    account_session_entity = await account_session_interactor.get(
        authentication_token_value=authentication_token_value,
    )

    return account_session_entity.account
