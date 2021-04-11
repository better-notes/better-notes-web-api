from fastapi import APIRouter
from fastapi.responses import JSONResponse

from web_api.accounts.dependencies import (
    ACCOUNT_AUTHENTICATE_USE_CASE_DEPENDENCY,
    ACCOUNT_REGISTER_USE_CASE_DEPENDENCY,
    ACCOUNT_SESSION_INTERACTOR_DEPENDENCY,
)
from web_api.accounts.usecases import (
    AccountAuthenticateUseCase,
    AccountRegisterUseCase,
    AccountSessionInteractor,
)
from web_api.accounts.values import (
    AuthenticationCredentialsValue,
    RegistrationCredentialsValue,
)

router = APIRouter()


@router.post('/account/register/')
async def register(
    registration_credentials: RegistrationCredentialsValue,
    account_register_use_case: AccountRegisterUseCase = (
        ACCOUNT_REGISTER_USE_CASE_DEPENDENCY
    ),
    user_session_interactor: AccountSessionInteractor = (
        ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
    ),
) -> JSONResponse:
    account_entity = await account_register_use_case.register(
        registration_credentials=registration_credentials,
    )
    user_session = await user_session_interactor.add(
        account_entity=account_entity,
    )

    response = JSONResponse(content={})
    response.set_cookie(
        key='authentication_token',
        value=user_session.token.value,
        httponly=True,
    )

    return response


@router.post('/account/authenticate/')
async def authenticate(
    authentication_credentials: AuthenticationCredentialsValue,
    account_authenticate_use_case: AccountAuthenticateUseCase = (
        ACCOUNT_AUTHENTICATE_USE_CASE_DEPENDENCY
    ),
    user_session_interactor: AccountSessionInteractor = (
        ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
    ),
) -> JSONResponse:
    user = await account_authenticate_use_case.authenticate(
        authentication_credentials=authentication_credentials,
    )
    user_session = await user_session_interactor.add(account_entity=user)

    response = JSONResponse(content={})
    response.set_cookie(
        key='authentication_token',
        value=user_session.token.value,
        httponly=True,
    )

    return response
