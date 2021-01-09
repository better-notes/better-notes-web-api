from fastapi import APIRouter

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
    AuthenticationTokenValue,
    RegistrationCredentialsValue,
)

router = APIRouter()


@router.post(
    '/account/register/', response_model=AuthenticationTokenValue,
)
async def register(
    registration_credentials: RegistrationCredentialsValue,
    account_register_use_case: AccountRegisterUseCase = (
        ACCOUNT_REGISTER_USE_CASE_DEPENDENCY
    ),
    user_session_interactor: AccountSessionInteractor = (
        ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
    ),
) -> AuthenticationTokenValue:
    account_entity = await account_register_use_case.register(
        registration_credentials=registration_credentials,
    )
    user_session = await user_session_interactor.add(
        account_entity=account_entity,
    )

    return user_session.token


@router.post(
    '/account/authenticate/', response_model=AuthenticationTokenValue,
)
async def authenticate(
    authentication_credentials: AuthenticationCredentialsValue,
    account_authenticate_use_case: AccountAuthenticateUseCase = (
        ACCOUNT_AUTHENTICATE_USE_CASE_DEPENDENCY
    ),
    user_session_interactor: AccountSessionInteractor = (
        ACCOUNT_SESSION_INTERACTOR_DEPENDENCY
    ),
) -> AuthenticationTokenValue:
    user = await account_authenticate_use_case.authenticate(
        authentication_credentials=authentication_credentials,
    )
    user_session = await user_session_interactor.add(account_entity=user)

    return user_session.token
