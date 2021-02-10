import abc
from typing import Any

from pydantic import BaseModel, validator


class Value(abc.ABC, BaseModel):  # noqa: WPS110
    """Base class for all value objects."""

    class Config:  # noqa WPS431
        extra = 'forbid'  # Forbid to pass unnecessary kwargs to constructor.


class Paging(Value):
    """Used to limit/offset results returned by views."""

    limit: int
    offset: int

    @validator('limit')
    @classmethod
    def validate_max_limit(cls, limit: int) -> int:
        max_limit = 20
        if limit > max_limit:
            raise ValueError(
                "Max limit can't be greater than {0}".format(max_limit),
            )

        return limit


class ErrorValue(Value):
    """Value for `validation_error_exception_handler`."""

    detail: list[dict[str, Any]]
