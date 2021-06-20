import secrets
from typing import Callable

from fastapi import Depends
from passlib.hash import bcrypt  # type: ignore

from web_api.accounts import repositories, usecases
from web_api.accounts.dependencies.repositories import (
    get_account_repository,
    get_account_session_repository,
)


def get_bcrypt() -> bcrypt:
    """Get bcrypt hasher."""
    return bcrypt


def get_account_register_use_case(
    user_repository: repositories.AccountRepository = Depends(get_account_repository),
    hasher: bcrypt = Depends(get_bcrypt),
) -> usecases.AccountRegisterUseCase:
    """Get account registration use case."""
    return usecases.AccountRegisterUseCase(user_repository=user_repository, hasher=hasher)


def get_account_authenticate_use_case(
    user_repository: repositories.AccountRepository = Depends(get_account_repository),
    hash_verifier: bcrypt = Depends(get_bcrypt),
) -> usecases.AccountAuthenticateUseCase:
    """Get account authentication use case."""
    return usecases.AccountAuthenticateUseCase(
        user_repository=user_repository, hash_verifier=hash_verifier,
    )


def get_account_session_id_generator() -> Callable[[], str]:
    """Get account session id generator."""
    return secrets.token_hex


def get_account_session_interactor(
    user_session_repository: repositories.AccountSessionRepository = Depends(
        get_account_session_repository,
    ),
    user_session_id_generator: Callable[[], str] = Depends(get_account_session_id_generator),
) -> usecases.AccountSessionInteractor:
    """Get account session interactor."""
    return usecases.AccountSessionInteractor(
        account_session_repository=user_session_repository,
        generate_user_session_id=user_session_id_generator,
    )
