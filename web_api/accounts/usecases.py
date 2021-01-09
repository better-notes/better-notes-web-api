import dataclasses
from typing import Callable

from fastapi import HTTPException, status
from passlib.ifc import PasswordHash

from web_api.accounts import entities, repositories, values
from web_api.accounts.specs import UsernameSpecification
from web_api.commons.values import Paging


@dataclasses.dataclass
class AccountRegisterUseCase:

    user_repository: repositories.AccountRepository
    hasher: PasswordHash

    async def register(
        self, *, registration_credentials: values.RegistrationCredentialsValue,
    ) -> entities.AccountEntity:
        password_hash = self.hasher.hash(registration_credentials.password1)

        user_entity, *_ = await self.user_repository.add(
            account_value_list=[
                values.AccountValue(
                    username=registration_credentials.username,
                    password_hash=password_hash,
                )
            ]
        )

        return user_entity


@dataclasses.dataclass
class UserDoesNotExistError(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'User with given username does not exist.'


@dataclasses.dataclass
class PasswordNotValidError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Password is not valid for given user'


@dataclasses.dataclass
class AccountAuthenticateUseCase:
    user_repository: repositories.AccountRepository
    hash_verifier: PasswordHash

    async def authenticate(
        self,
        *,
        authentication_credentials: values.AuthenticationCredentialsValue,
    ) -> entities.AccountEntity:
        account_entities = await self.user_repository.get(
            spec=UsernameSpecification(
                username=authentication_credentials.username,
            ),
            paging=Paging(limit=1, offset=0),
        )
        if not account_entities:
            raise UserDoesNotExistError()

        account_entity = account_entities[0]
        password_hash = await self.user_repository.get_password_hash(
            account_entity=account_entity,
        )
        password_valid = self.hash_verifier.verify(
            secret=authentication_credentials.password, hash=password_hash,
        )

        if not password_valid:
            raise PasswordNotValidError()

        return account_entity


@dataclasses.dataclass
class SessionNotFoundError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Session with given token does not exist'


@dataclasses.dataclass
class AccountSessionInteractor:
    account_session_repository: repositories.AccountSessionRepository
    generate_user_session_id: Callable[[], str]

    async def get(
        self, *, authentication_token_value: values.AuthenticationTokenValue,
    ) -> entities.AccountSessionEntity:
        user_sessions = await self.account_session_repository.get(
            authentication_token_value_list=[authentication_token_value],
        )
        if not user_sessions:
            raise SessionNotFoundError()

        return user_sessions[0]

    async def add(
        self, *, account_entity: entities.AccountEntity,
    ) -> entities.AccountSessionEntity:
        session_id = self.generate_user_session_id()
        account_session = entities.AccountSessionEntity(
            token=values.AuthenticationTokenValue(value=session_id),
            account=account_entity,
        )
        account_sessions = await self.account_session_repository.add(
            account_session_entity_list=[account_session],
        )

        return account_sessions[0]
