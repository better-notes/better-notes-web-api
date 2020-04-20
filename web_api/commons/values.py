import abc
import dataclasses
from typing import Any


class Value(abc.ABC):
    """TODO:"""


@dataclasses.dataclass
class ID(Value):
    """TODO:"""

    value: Any
