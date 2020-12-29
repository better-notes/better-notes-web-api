import abc
from pydantic import BaseModel


class Value(abc.ABC, BaseModel):
    """TODO:"""

    class Config:
        extra = 'forbid'


class Paging(Value):
    """Used to limit/offset results returned by views."""

    limit: int
    offset: int
