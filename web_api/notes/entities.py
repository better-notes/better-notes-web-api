import dataclasses
from typing import Any, Dict, List

from funcy import lmap

from web_api.commons import entities


@dataclasses.dataclass
class Tag(entities.Entity):
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tag':
        return cls(**data)


@dataclasses.dataclass
class Note(entities.Entity):
    text: str
    tags: List[Tag]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Note':
        return cls(tags=lmap(Tag.from_dict, data.pop('tags')), **data)
