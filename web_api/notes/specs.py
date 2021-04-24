import dataclasses
from typing import Any

import bson

from web_api.commons.specs import Specification
from web_api.notes.values import TagValue


@dataclasses.dataclass
class NoteSpecification(Specification):
    """Return all notes."""

    def get_query(self) -> dict[str, Any]:
        """Get empty query."""
        return {}


@dataclasses.dataclass
class GetNoteSpecification(NoteSpecification):
    # XXX: help me with naming
    """Return all notes for given username."""

    username: str

    def get_query(self) -> dict[str, Any]:
        """Get username filtered query."""
        return {'account.username': self.username}


@dataclasses.dataclass
class GetNoteByTagsSpecification(NoteSpecification):
    """Return all notes with given tags."""

    tag_value_list: list[TagValue]

    def get_query(self) -> dict[str, Any]:
        """Get query matching documents with all given tags."""
        tags = [tag_value.dict() for tag_value in self.tag_value_list]

        return {'tags': {'$all': tags}}


@dataclasses.dataclass
class UpdateNoteSpecification(NoteSpecification):
    """Update all notes for given username w/ given id."""

    # XXX: help me with naming
    username: str
    _id: bson.ObjectId

    def get_query(self) -> dict[str, Any]:
        """Get username & _id filtered query."""
        return {'account.username': self.username, '_id': self._id}


@dataclasses.dataclass
class DeleteNoteSpecification(NoteSpecification):
    """Delete all notes for given username w/ given ids."""

    # XXX: help me with naming
    username: str
    object_id_list: list[bson.ObjectId]

    def get_query(self) -> dict[str, Any]:
        """Get username & object_id_list filtered query."""
        return {
            'account.username': self.username,
            '_id': {'$in': self.object_id_list},
        }
