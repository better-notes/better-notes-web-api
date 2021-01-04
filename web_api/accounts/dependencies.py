import secrets
from typing import Callable
from aioredis import create_redis_pool
from aioredis.commands import Redis
from fastapi import Depends
from motor import motor_asyncio  # type: ignore
from passlib.hash import bcrypt  # type: ignore
from web_api.accounts import repositories, usecases
from web_api.commons.dependencies import get_mongo_client
from web_api.settings import Settings


def get_user_repository(
    client: motor_asyncio.AsyncIOMotorClient = Depends(get_mongo_client),
    settings: Settings = Depends(lambda: Settings()),
) -> repositories.UserRepository:
    return repositories.UserRepository(client=client, settings=settings)


def get_bcrypt() -> bcrypt:
    return bcrypt


def get_account_register_use_case(
    user_repository: repositories.UserRepository = Depends(
        get_user_repository
    ),
    hasher: bcrypt = Depends(get_bcrypt),
) -> usecases.AccountRegisterUseCase:
    return usecases.AccountRegisterUseCase(
        user_repository=user_repository, hasher=hasher
    )


def get_account_authenticate_use_case(
    user_repository: repositories.UserRepository = Depends(
        get_user_repository
    ),
    hash_verifier: bcrypt = Depends(get_bcrypt),
) -> usecases.AccountAuthenticateUseCase:
    return usecases.AccountAuthenticateUseCase(
        user_repository=user_repository, hash_verifier=hash_verifier
    )


async def get_redis(settings: Settings = Depends(lambda: Settings())) -> Redis:
    return await create_redis_pool(settings.REDIS_ADDRESS)


def get_user_session_repository(
    client: Redis = Depends(get_redis),
) -> repositories.UserSessionRepository:
    return repositories.UserSessionRepository(client=client)


def get_account_session_id_generator() -> Callable[[], str]:
    return secrets.token_hex


def get_account_session_interactor(
    user_session_repository: repositories.UserSessionRepository = Depends(
        get_user_session_repository
    ),
    user_session_id_generator: Callable[[], str] = Depends(
        get_account_session_id_generator
    ),
) -> usecases.AccountSessionInteractor:
    return usecases.AccountSessionInteractor(
        user_session_repository=user_session_repository,
        generate_user_session_id=user_session_id_generator,
    )
