from web_api.commons import values


class TagValue(values.Value):
    """Value object to add note's tags."""

    name: str


class NoteValue(values.Value):
    """Value object to add notes."""

    text: str
    tags: list[TagValue]
