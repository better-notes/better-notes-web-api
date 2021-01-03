from pydantic import validator
from web_api.commons import values


class RegistrationCredentials(values.Value):
    username: str
    password1: str
    password2: str

    @validator('password2')
    def passwords_match(cls, password2: str, values: dict[str, str]) -> str:
        if 'password1' in values and password2 != values['password1']:
            raise ValueError('passwords do not match')

        return password2


class AuthenticationCredentials(values.Value):
    username: str
    password: str


class AuthenticationToken(values.Value):
    value: str


class UserValue(values.Value):
    username: str
    password_hash: str
