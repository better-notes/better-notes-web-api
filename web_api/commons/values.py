import abc

from pydantic import BaseModel, validator


class Value(abc.ABC, BaseModel):
    """TODO:"""

    class Config:
        extra = 'forbid'


class Paging(Value):
    """Used to limit/offset results returned by views."""

    limit: int
    offset: int

    @validator('limit')
    def validate_max_limit(cls, limit: int) -> int:
        max_limit = 20
        if limit > max_limit:
            raise ValueError(f'Max limit can\'t be greater than {max_limit}')

        return limit
