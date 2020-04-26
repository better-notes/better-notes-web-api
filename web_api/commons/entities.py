import dataclasses
from datetime import datetime

from web_api.commons import values


@dataclasses.dataclass
class Entity(values.Value):
    """TODO:"""

    id_: values.ID
    created_at: datetime
