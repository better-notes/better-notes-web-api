from fastapi import status
from syrupy.filters import props

from web_api.accounts.dependencies import get_account_session_id_generator
from web_api.accounts.tests.factories.repository_factories import (
    AccountRepositoryFactory,
)
from web_api.accounts.tests.factories.usecase_factories import (
    AccountRegisterUseCaseFactory,
)
from web_api.accounts.tests.factories.value_factories import (
    AccountValueFactory,
    AuthenticationCredentialsValueFactory,
    RegistrationCredentialsValueFactory,
)


async def test_register(client, app, reverse_route, snapshot):
    app.dependency_overrides[
        get_account_session_id_generator
    ] = lambda: lambda: 'session_id'

    registration_credentials = RegistrationCredentialsValueFactory()
    response = await client.post(
        reverse_route('register'), json=registration_credentials.dict(),
    )

    assert response.json() == snapshot(exclude=props('id_', 'created_at'))
    assert response.status_code == status.HTTP_200_OK


async def test_register_duplicate_username(
    client, app, reverse_route, snapshot,
):
    app.dependency_overrides[
        get_account_session_id_generator
    ] = lambda: lambda: 'session_id'

    test_username = 'test username'

    account_repository = AccountRepositoryFactory()
    account_value = AccountValueFactory(username=test_username)

    await account_repository.add(account_value_list=[account_value])

    registration_credentials = RegistrationCredentialsValueFactory(
        username=test_username,
    )
    response = await client.post(
        reverse_route('register'), json=registration_credentials.dict(),
    )

    assert response.json() == snapshot(exclude=props('id_', 'created_at'))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_authenticate(client, app, reverse_route, snapshot):
    app.dependency_overrides[
        get_account_session_id_generator
    ] = lambda: lambda: 'session_id'

    password = 'test_password'
    registration_credentials = RegistrationCredentialsValueFactory(
        password1=password, password2=password
    )
    account_register_use_case = AccountRegisterUseCaseFactory()
    user_entity = await account_register_use_case.register(
        registration_credentials=registration_credentials
    )

    authentication_credentials = AuthenticationCredentialsValueFactory(
        username=user_entity.username, password=password
    )
    response = await client.post(
        reverse_route('authenticate'), json=authentication_credentials.dict()
    )

    assert response.json() == snapshot(exclude=props('id_', 'created_at'))
