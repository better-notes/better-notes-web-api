from fastapi.param_functions import Cookie

from web_api.accounts.values import AuthenticationTokenValue


def get_authentication_token_value(
    authentication_token: str = Cookie(...),
) -> AuthenticationTokenValue:
    """Get authentication token value from cookie."""
    return AuthenticationTokenValue(value=authentication_token)
