import abc
from typing import Any


class Specification(abc.ABC):
    """TODO:"""

    @abc.abstractmethod
    def get_query(self) -> Any:
        raise NotImplementedError
