from fastapi.param_functions import Depends
from motor import motor_asyncio

from web_api.commons.values import Paging
from web_api.settings import Settings


def get_settings():
    """Get settings."""
    return Settings()


async def get_mongo_client(
    settings: Settings = Depends(get_settings),
) -> motor_asyncio.AsyncIOMotorClient:
    """Get mongo client."""
    # XXX: async b/c motor client requires loop for instantiation ¯\_(ツ)_/¯
    return motor_asyncio.AsyncIOMotorClient(settings.mongo_host, settings.mongo_port)


async def get_paging(limit: int, offset: int) -> Paging:
    """Get paging from query params."""
    return Paging(limit=limit, offset=offset)
