import abc

from pydantic import BaseModel


class Value(abc.ABC, BaseModel):
    """TODO:"""

    class Config:
        extra = 'forbid'
