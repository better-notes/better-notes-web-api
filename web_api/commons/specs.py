import abc
from typing import Any


class Specification(abc.ABC):
    """Get all entities filtered by query."""

    @abc.abstractmethod
    def get_query(self) -> dict[str, Any]:
        """Get query."""
        raise NotImplementedError()  # noqa: DAR401
