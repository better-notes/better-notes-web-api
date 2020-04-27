import asyncio

import factory
import pytest
from motor import motor_asyncio

from web_api import settings


@pytest.fixture(autouse=True, scope='function')  # type: ignore
def reset_sequence() -> None:
    """Reset any factory sequence before each test start."""
    for factory_ in factory.Factory.__subclasses__():
        factory_.reset_sequence(0)


@pytest.fixture
def motor_client(loop):  # type: ignore
    return motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_HOST, settings.MONGO_PORT, io_loop=loop
    )


@pytest.fixture(autouse=True)
async def clear_mongo(motor_client):  # type: ignore
    """Clear mongodb before and after each test."""
    motor_client.drop_database(settings.MONGO_DATABASE)
    yield
    motor_client.drop_database(settings.MONGO_DATABASE)


@pytest.fixture(autouse=True)
def set_event_loop(loop):
    asyncio.set_event_loop(loop)
