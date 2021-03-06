import asyncio

import pytest
from httpx import AsyncClient
from motor import motor_asyncio

from web_api.commons.tests.factories import BaseFactory
from web_api.indexes import create_indexes
from web_api.main import get_application
from web_api.settings import Settings


@pytest.fixture(autouse=True, scope='function')  # type: ignore
def reset_sequence() -> None:
    """Reset any factory sequence before each test start."""
    for factory_class in BaseFactory.__subclasses__():
        factory_class.reset_sequence(0)


@pytest.fixture
async def motor_client():  # type: ignore
    """Client for mongo."""
    settings = Settings()
    loop = asyncio.get_event_loop()

    return motor_asyncio.AsyncIOMotorClient(
        settings.mongo_host, settings.mongo_port, io_loop=loop,
    )


@pytest.fixture(autouse=True)
async def clear_mongo(
    motor_client: motor_asyncio.AsyncIOMotorClient,  # noqa: WPS442
):
    """Clear mongodb before and after each test."""
    settings = Settings()
    await motor_client.drop_database(settings.mongo_database)
    await create_indexes(
        motor_client[settings.mongo_database], settings=settings,
    )
    yield
    await motor_client.drop_database(settings.mongo_database)


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
