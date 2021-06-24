import aioredis
from aioredis.commands import Redis
from fastapi import Depends
from motor import motor_asyncio

from web_api.accounts import repositories
from web_api.commons.dependencies import get_mongo_client, get_settings
from web_api.settings import Settings


def get_account_repository(
    client: motor_asyncio.AsyncIOMotorClient = Depends(get_mongo_client),
    settings: Settings = Depends(get_settings),
) -> repositories.AccountRepository:
    """Get account repository."""
    return repositories.AccountRepository(client=client, settings=settings)


async def get_redis(settings: Settings = Depends(get_settings)) -> Redis:
    """Get redis client."""
    pool = await aioredis.create_redis_pool(settings.redis_address)
    yield pool
    pool.close()
    await pool.wait_closed()


def get_account_session_repository(
    client: Redis = Depends(get_redis),
) -> repositories.AccountSessionRepository:
    """Get account session repository."""
    return repositories.AccountSessionRepository(client=client)
