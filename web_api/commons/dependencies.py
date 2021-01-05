from fastapi.param_functions import Depends
from motor import motor_asyncio

from web_api.commons.values import Paging
from web_api.settings import Settings


async def _get_mongo_client(
    settings: Settings = Depends(lambda: Settings()),
) -> motor_asyncio.AsyncIOMotorClient:
    # XXX: async b/c motor client requires loop for instantiation ¯\_(ツ)_/¯
    return motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_HOST, settings.MONGO_PORT,
    )


MONGO_CLIENT_DEPENDENCY = Depends(_get_mongo_client)


def _get_settings():
    return Settings()


SETTINGS_DEPENDENCY = Depends(_get_settings)


PAGING_DEPENDENCY = Depends(Paging)
