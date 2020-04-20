import asyncio
import pytest
from motor import motor_asyncio
from web_api import settings


@pytest.fixture  # type: ignore
def motor_client(
    loop: asyncio.AbstractEventLoop,
) -> motor_asyncio.AsyncIOMotorClient:
    return motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_HOST, settings.MONGO_PORT, io_loop=loop
    )
