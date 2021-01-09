import dataclasses
from typing import Any

from web_api.commons.specs import Specification


@dataclasses.dataclass
class UsernameSpecification(Specification):
    """Get all users by username."""

    username: str

    def get_query(self) -> dict[str, Any]:
        """Get query."""
        return {'username': self.username}
