import dataclasses
from typing import List

from web_api.commons import values


@dataclasses.dataclass
class Tag(values.Value):
    name: str


@dataclasses.dataclass
class Note(values.Value):
    text: str
    tags: List[Tag]
