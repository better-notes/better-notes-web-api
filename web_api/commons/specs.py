import abc
import dataclasses
from typing import Any, TypeVar, cast


class Specification(abc.ABC):
    """Get all entities filtered by query."""

    @abc.abstractmethod
    def get_query(self) -> dict[str, Any]:
        """Get query."""
        raise NotImplementedError()  # noqa: DAR401


@dataclasses.dataclass
class MergedSpecification(Specification):
    """Get entities by all given specifications."""

    specs: tuple[Specification, ...]

    def get_query(self) -> dict[str, Any]:
        """Concatenate queries from all specs."""
        query = {}
        for spec in self.specs:
            query.update(spec.get_query())

        return query


Type = TypeVar('Type', bound=Specification)


def merge_specs(*specs: Type) -> Type:
    """Get any number of specs & merge them to MergedSpecification."""
    return cast(Type, MergedSpecification(specs=specs))
