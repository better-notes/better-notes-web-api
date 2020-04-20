import dataclasses
from datetime import datetime

from web_api.commons import values


@dataclasses.dataclass
class Entity:
    """TODO:"""

    id_: values.ID
    created_at: datetime
