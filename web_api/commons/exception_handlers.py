from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from web_api.commons.values import ErrorValue


async def validation_error_exception_handler(
    request: Request, exception: ValidationError,
) -> JSONResponse:
    """
    Dirty hack.

    Rewrite if errors didn't match schema of `Unprocessable Entity`.
    """
    return JSONResponse(
        ErrorValue(detail=exception.errors()).dict(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
