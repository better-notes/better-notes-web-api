import asyncio
import inspect

import factory
from aioredis.commands import Redis, create_redis
from motor import motor_asyncio

from web_api.settings import Settings


class AsyncFactory(factory.Factory):
    """Factory capable of creating objects w/ async functions."""

    # TODO: move to commons if other applications would benefit from it

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():  # noqa: WPS430
            for key, value in kwargs.items():  # noqa: WPS110
                if inspect.isawaitable(value):
                    kwargs[key] = await value
            return model_class(*args, **kwargs)

        return asyncio.create_task(maker_coroutine())


class SettingsFactory(factory.Factory):
    # TODO: #11 move settings factory to commons
    class Meta:
        model = Settings


class MotorClientFactory(factory.Factory):
    # TODO: #12 move motor client factory to commons
    class Meta:
        model = motor_asyncio.AsyncIOMotorClient

    host = 'localhost'
    port = 27017
    io_loop = factory.LazyFunction(asyncio.get_event_loop)


class RedisPoolFactory(AsyncFactory):
    class Meta:
        model = Redis

    address = 'redis://localhost:6379'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():  # noqa: WPS430
            return await create_redis(*args, **kwargs)

        return asyncio.create_task(maker_coroutine())
