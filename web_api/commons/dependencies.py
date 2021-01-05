from fastapi.param_functions import Depends
from motor import motor_asyncio
from web_api.settings import Settings


async def get_mongo_client(
    settings: Settings = Depends(lambda: Settings()),
) -> motor_asyncio.AsyncIOMotorClient:
    # XXX: async b/c motor client requires loop for instantiation ¯\_(ツ)_/¯
    return motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_HOST, settings.MONGO_PORT,
    )
