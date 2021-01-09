import factory

from web_api.accounts.repositories import (
    AccountRepository,
    AccountSessionRepository,
)
from web_api.commons.tests.factories import (
    AsyncFactory,
    MotorClientFactory,
    RedisPoolFactory,
    SettingsFactory,
)


class AccountRepositoryFactory(factory.Factory):
    class Meta:
        model = AccountRepository

    client = factory.SubFactory(MotorClientFactory)
    settings = factory.SubFactory(SettingsFactory)


class AccountSessionRepositoryFactory(AsyncFactory):
    class Meta:
        model = AccountSessionRepository

    client = factory.SubFactory(RedisPoolFactory)
