from syrupy.filters import props

from web_api.accounts.dependencies import get_account_session_id_generator
from web_api.accounts.tests.factories import (
    AccountRegisterUseCaseFactory,
    AuthenticationCredentialsValueFactory,
    RegistrationCredentialsValueFactory,
)


async def test_register(client, app, reverse_route, snapshot):
    app.dependency_overrides[
        get_account_session_id_generator
    ] = lambda: lambda: 'session_id'

    registration_credentials = RegistrationCredentialsValueFactory()
    response = await client.post(
        reverse_route('register'), json=registration_credentials.dict()
    )

    assert response.json() == snapshot(exclude=props('id_', 'created_at'))


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
