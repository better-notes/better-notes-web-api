from pydantic import validator

from web_api.commons import values


class RegistrationCredentialsValue(values.Value):
    username: str
    password1: str
    password2: str

    @validator('password2')
    def passwords_match(cls, password2: str, values: dict[str, str]) -> str:
        if 'password1' in values and password2 != values['password1']:
            raise ValueError('passwords do not match')

        return password2


class AuthenticationCredentialsValue(values.Value):
    username: str
    password: str


class AuthenticationTokenValue(values.Value):
    value: str


class AccountValue(values.Value):
    """Account value. Used to add/update accounts."""

    username: str
    password_hash: str
