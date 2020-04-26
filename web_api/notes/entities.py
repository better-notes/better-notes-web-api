import dataclasses
from typing import Any, Dict, List

from funcy import lmap

from web_api.commons import entities


@dataclasses.dataclass
class TagEntity(entities.Entity):
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TagEntity':
        return cls(**data)


@dataclasses.dataclass
class NoteEntity(entities.Entity):
    text: str
    tags: List[TagEntity]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NoteEntity':
        return cls(tags=lmap(TagEntity.from_dict, data.pop('tags')), **data)
