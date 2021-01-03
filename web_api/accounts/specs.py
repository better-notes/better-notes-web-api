import dataclasses

from web_api.commons.specs import Specification


@dataclasses.dataclass
class GetUserByUsernameSpecification(Specification):
    username: str

    def get_query(self) -> dict[str, str]:
        return {'username': self.username}
