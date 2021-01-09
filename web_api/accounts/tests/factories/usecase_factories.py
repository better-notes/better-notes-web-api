import secrets

import factory
from passlib.hash import bcrypt  # type: ignore

from web_api.accounts.tests.factories.repository_factories import (
    AccountRepositoryFactory,
    AccountSessionRepositoryFactory,
)
from web_api.accounts.usecases import (
    AccountRegisterUseCase,
    AccountSessionInteractor,
)
from web_api.commons.tests.factories import AsyncFactory


class AccountRegisterUseCaseFactory(factory.Factory):
    class Meta:
        model = AccountRegisterUseCase

    user_repository = factory.SubFactory(AccountRepositoryFactory)
    hasher = factory.LazyFunction(lambda: bcrypt)


class AccountSessionInteractorFactory(AsyncFactory):
    class Meta:
        model = AccountSessionInteractor

    account_session_repository = factory.SubFactory(
        AccountSessionRepositoryFactory,
    )
    generate_user_session_id = factory.LazyFunction(lambda: secrets.token_hex)
