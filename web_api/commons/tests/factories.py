import asyncio
import inspect
from typing import Any, Generic, TypeVar

import factory
from aioredis.commands import Redis, create_redis
from motor import motor_asyncio

from web_api.settings import Settings

Type = TypeVar('Type')


class BaseFactory(
    Generic[Type], factory.base.BaseFactory, metaclass=factory.base.FactoryMetaClass,
):
    class Meta(factory.base.BaseMeta):
        """Base meta."""

    def __new__(cls, *args: Any, **kwargs: Any) -> Type:  # noqa: WPS612
        return super().__new__(*args, **kwargs)  # type: ignore


class AsyncFactory(factory.Factory):
    """Factory capable of creating objects w/ async functions."""

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

        return asyncio.ensure_future(maker_coroutine())


class SettingsFactory(BaseFactory[motor_asyncio.AsyncIOMotorClient]):
    class Meta:
        model = Settings


class MotorClientFactory(BaseFactory[motor_asyncio.AsyncIOMotorClient]):
    class Meta:
        model = motor_asyncio.AsyncIOMotorClient

    host = 'localhost'
    port = 27017
    io_loop = factory.LazyFunction(asyncio.get_event_loop)


class RedisPoolFactory(BaseFactory[Redis], AsyncFactory):
    class Meta:
        model = Redis

    address = 'redis://localhost:6379'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():  # noqa: WPS430
            return await create_redis(*args, **kwargs)

        return asyncio.create_task(maker_coroutine())
