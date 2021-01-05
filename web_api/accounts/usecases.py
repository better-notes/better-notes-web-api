import dataclasses
from typing import Callable

from fastapi import HTTPException, status
from passlib.ifc import PasswordHash

from web_api.accounts import entities, repositories, values
from web_api.accounts.specs import UsernameSpecification
from web_api.commons.values import Paging


@dataclasses.dataclass
class AccountRegisterUseCase:

    user_repository: repositories.UserRepository
    hasher: PasswordHash

    async def register(
        self, *, registration_credentials: values.RegistrationCredentialsValue
    ) -> entities.AccountEntity:
        password_hash = self.hasher.hash(registration_credentials.password1)

        user_entity, *_ = await self.user_repository.add(
            [
                values.UserValue(
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
    user_repository: repositories.UserRepository
    hash_verifier: PasswordHash

    async def authenticate(
        self,
        *,
        authentication_credentials: values.AuthenticationCredentialsValue
    ) -> entities.AccountEntity:
        user_entities = await self.user_repository.get(
            spec=UsernameSpecification(
                username=authentication_credentials.username
            ),
            paging=Paging(limit=1, offset=0),
        )
        if len(user_entities) == 0:
            raise UserDoesNotExistError()

        user_entity = user_entities[0]
        password_valid = self.hash_verifier.verify(
            secret=authentication_credentials.password,
            hash=user_entity.password_hash,
        )

        if not password_valid:
            raise PasswordNotValidError()

        return user_entity


@dataclasses.dataclass
class SessionNotFoundError(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Session with given token does not exist'


@dataclasses.dataclass
class AccountSessionInteractor:
    user_session_repository: repositories.UserSessionRepository
    generate_user_session_id: Callable[[], str]

    async def get(
        self, *, token: values.AuthenticationTokenValue
    ) -> entities.AccountSessionEntity:
        user_sessions = await self.user_session_repository.get(values=[token])
        if len(user_sessions) == 0:
            raise SessionNotFoundError()

        return user_sessions[0]

    async def add(
        self, *, user: entities.AccountEntity
    ) -> entities.AccountSessionEntity:
        session_id = self.generate_user_session_id()
        user_session = entities.AccountSessionEntity(
            token=values.AuthenticationTokenValue(value=session_id), user=user
        )
        user_sessions = await self.user_session_repository.add(
            entities=[user_session]
        )

        return user_sessions[0]
