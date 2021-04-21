from web_api.accounts.values import (
    AccountValue,
    AuthenticationCredentialsValue,
    RegistrationCredentialsValue,
)
from web_api.commons.tests.factories import BaseFactory


class RegistrationCredentialsValueFactory(
    BaseFactory[RegistrationCredentialsValue],
):
    class Meta:
        model = RegistrationCredentialsValue

    username = 'test_username'
    password1 = 'test_password'
    password2 = 'test_password'


class AuthenticationCredentialsValueFactory(
    BaseFactory[AuthenticationCredentialsValue],
):
    class Meta:
        model = AuthenticationCredentialsValue

    username = 'test_username'
    password = 'test_password'  # noqa: S105


class AccountValueFactory(BaseFactory[AccountValue]):
    class Meta:
        model = AccountValue

    username = 'test_username'
    password_hash = 'test_password_hash'  # noqa: S105
