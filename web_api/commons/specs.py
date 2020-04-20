import abc
from typing import Dict, Any


class Specification(abc.ABC):
    """TODO:"""

    @abc.abstractmethod
    def get_query(self) -> Dict[str, Any]:
        raise NotImplementedError
