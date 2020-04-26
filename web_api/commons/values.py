import abc
import dataclasses
from typing import Any, Dict


class Value(abc.ABC):
    """TODO:"""

    def as_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class ID(Value):
    """TODO:"""

    value: Any
