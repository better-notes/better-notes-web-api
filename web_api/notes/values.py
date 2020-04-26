import dataclasses
from typing import List

from web_api.commons import values


@dataclasses.dataclass
class TagValue(values.Value):
    name: str


@dataclasses.dataclass
class NoteValue(values.Value):
    text: str
    tags: List[TagValue]
