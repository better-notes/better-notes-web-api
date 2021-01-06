from fastapi import APIRouter
from fastapi.param_functions import Depends

from web_api.accounts.dependencies import (
    get_account_authenticate_use_case,
    get_account_register_use_case,
    get_account_session_interactor,
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
    account_register_use_case: AccountRegisterUseCase = Depends(
        get_account_register_use_case
    ),
    user_session_interactor: AccountSessionInteractor = Depends(
        get_account_session_interactor
    ),
) -> AuthenticationTokenValue:
    user = await account_register_use_case.register(
        registration_credentials=registration_credentials
    )
    user_session = await user_session_interactor.add(user=user)

    return user_session.token


@router.post(
    '/account/authenticate/', response_model=AuthenticationTokenValue,
)
async def authenticate(
    authentication_credentials: AuthenticationCredentialsValue,
    account_authenticate_use_case: AccountAuthenticateUseCase = Depends(
        get_account_authenticate_use_case
    ),
    user_session_interactor: AccountSessionInteractor = Depends(
        get_account_session_interactor
    ),
) -> AuthenticationTokenValue:
    user = await account_authenticate_use_case.authenticate(
        authentication_credentials=authentication_credentials
    )
    user_session = await user_session_interactor.add(user=user)

    return user_session.token
