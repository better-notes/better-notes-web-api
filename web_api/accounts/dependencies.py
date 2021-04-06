import secrets
from typing import Callable

from aioredis import create_redis
from aioredis.commands import Redis
from fastapi import Depends
from fastapi.param_functions import Header
from motor import motor_asyncio  # type: ignore
from passlib.hash import bcrypt  # type: ignore

from web_api.accounts import repositories, usecases
from web_api.commons.dependencies import (
    MONGO_CLIENT_DEPENDENCY,
    SETTINGS_DEPENDENCY,
)
from web_api.settings import Settings


def get_user_repository(
    client: motor_asyncio.AsyncIOMotorClient = MONGO_CLIENT_DEPENDENCY,
    settings: Settings = SETTINGS_DEPENDENCY,
) -> repositories.AccountRepository:
    return repositories.AccountRepository(client=client, settings=settings)


ACCOUNT_REPOSITORY_DEPENDENCY = Depends(get_user_repository)


def get_bcrypt() -> bcrypt:
    return bcrypt


BCRYPT_DEPENDENCY = Depends(get_bcrypt)


def get_account_register_use_case(
    user_repository: repositories.AccountRepository = (
        ACCOUNT_REPOSITORY_DEPENDENCY
    ),
    hasher: bcrypt = BCRYPT_DEPENDENCY,
) -> usecases.AccountRegisterUseCase:
    return usecases.AccountRegisterUseCase(
        user_repository=user_repository, hasher=hasher,
    )


ACCOUNT_REGISTER_USE_CASE_DEPENDENCY = Depends(get_account_register_use_case)


def get_account_authenticate_use_case(
    user_repository: repositories.AccountRepository = (
        ACCOUNT_REPOSITORY_DEPENDENCY
    ),
    hash_verifier: bcrypt = BCRYPT_DEPENDENCY,
) -> usecases.AccountAuthenticateUseCase:
    return usecases.AccountAuthenticateUseCase(
        user_repository=user_repository, hash_verifier=hash_verifier,
    )


ACCOUNT_AUTHENTICATE_USE_CASE_DEPENDENCY = Depends(
    get_account_authenticate_use_case,
)


async def get_redis(settings: Settings = SETTINGS_DEPENDENCY) -> Redis:
    return await create_redis(settings.redis_address)


REDIS_DEPENDENCY = Depends(get_redis)


def _get_user_session_repository(
    client: Redis = REDIS_DEPENDENCY,
) -> repositories.AccountSessionRepository:
    return repositories.AccountSessionRepository(client=client)


USER_SESSION_REPOSITORY_DEPENDENCY = Depends(_get_user_session_repository)


def get_account_session_id_generator() -> Callable[[], str]:
    return secrets.token_hex


ACCOUNT_SESSION_ID_GENERATOR_DEPENDENCY = Depends(
    get_account_session_id_generator,
)


def get_account_session_interactor(
    user_session_repository: repositories.AccountSessionRepository = (
        USER_SESSION_REPOSITORY_DEPENDENCY
    ),
    user_session_id_generator: Callable[[], str] = (
        ACCOUNT_SESSION_ID_GENERATOR_DEPENDENCY
    ),
) -> usecases.AccountSessionInteractor:
    return usecases.AccountSessionInteractor(
        account_session_repository=user_session_repository,
        generate_user_session_id=user_session_id_generator,
    )


ACCOUNT_SESSION_INTERACTOR_DEPENDENCY = Depends(
    get_account_session_interactor,
)


AUTHORIZATION_TOKEN_HEADER_DEPENDENCY = Header(...)
