from fastapi import APIRouter
from fastapi.param_functions import Depends
from web_api.accounts.dependencies import (
    get_account_authenticate_use_case,
    get_account_register_use_case,
    get_user_session_interactor,
)
from web_api.accounts.usecases import (
    AccountAuthenticateUseCase,
    AccountRegisterUseCase,
    UserSessionInteractor,
)
from web_api.accounts.values import (
    AuthenticationCredentials,
    AuthenticationToken,
    RegistrationCredentials,
)

router = APIRouter()


@router.post(
    '/account/register/', response_model=AuthenticationToken,
)
async def register(
    registration_credentials: RegistrationCredentials,
    account_register_use_case: AccountRegisterUseCase = Depends(
        get_account_register_use_case
    ),
    user_session_interactor: UserSessionInteractor = Depends(
        get_user_session_interactor
    ),
) -> AuthenticationToken:
    user = await account_register_use_case.register(
        registration_credentials=registration_credentials
    )
    user_session = await user_session_interactor.add(user=user)

    return user_session.token


@router.post(
    '/account/authenticate/', response_model=AuthenticationToken,
)
async def authenticate(
    authentication_credentials: AuthenticationCredentials,
    account_authenticate_use_case: AccountAuthenticateUseCase = Depends(
        get_account_authenticate_use_case
    ),
    user_session_interactor: UserSessionInteractor = Depends(
        get_user_session_interactor
    ),
) -> AuthenticationToken:
    user = await account_authenticate_use_case.authenticate(
        authentication_credentials=authentication_credentials
    )
    user_session = await user_session_interactor.add(user=user)

    return user_session.token
