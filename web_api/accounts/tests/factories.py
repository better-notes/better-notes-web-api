import asyncio

import factory
from motor import motor_asyncio
from passlib.hash import bcrypt  # type: ignore
from web_api.accounts.repositories import UserRepository
from web_api.accounts.usecases import AccountRegisterUseCase
from web_api.accounts.values import (
    AuthenticationCredentials,
    RegistrationCredentials,
)
from web_api.settings import Settings


class RegistrationCredentialsFactory(factory.Factory):
    class Meta:
        model = RegistrationCredentials

    username = 'test_username'
    password1 = 'test_password'
    password2 = 'test_password'


class AuthenticationCredentialsFactory(factory.Factory):
    class Meta:
        model = AuthenticationCredentials

    username = 'test_username'
    password = 'test_password'


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


class UserRepositoryFactory(factory.Factory):
    class Meta:
        model = UserRepository

    client = factory.SubFactory(MotorClientFactory)
    settings = factory.SubFactory(SettingsFactory)


class AccountRegisterUseCaseFactory(factory.Factory):
    class Meta:
        model = AccountRegisterUseCase

    user_repository = factory.SubFactory(UserRepositoryFactory)
    hasher = factory.LazyFunction(lambda: bcrypt)
