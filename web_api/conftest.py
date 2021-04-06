import asyncio

import factory
import pytest
from httpx import AsyncClient
from motor import motor_asyncio

from web_api.indexes import create_indexes
from web_api.main import get_application
from web_api.settings import Settings


@pytest.fixture(autouse=True, scope='function')  # type: ignore
def reset_sequence() -> None:
    """Reset any factory sequence before each test start."""
    for factory_ in factory.Factory.__subclasses__():
        factory_.reset_sequence(0)


@pytest.fixture
async def motor_client():  # type: ignore
    settings = Settings()
    loop = asyncio.get_event_loop()

    return motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_HOST, settings.MONGO_PORT, io_loop=loop
    )


@pytest.fixture(autouse=True)
async def clear_mongo(motor_client: motor_asyncio.AsyncIOMotorClient):
    """Clear mongodb before and after each test."""
    settings = Settings()
    await motor_client.drop_database(settings.MONGO_DATABASE)
    await create_indexes(
        motor_client[settings.MONGO_DATABASE], settings=settings,
    )
    yield
    await motor_client.drop_database(settings.MONGO_DATABASE)


@pytest.fixture
def app():
    return get_application()


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.fixture
def reverse_route(app):
    def _reverse_route(route_name, *args, **kwargs):
        return app.url_path_for(route_name, *args, **kwargs)

    return _reverse_route
