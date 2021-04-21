from web_api.commons import values


class TagValue(values.Value):
    """Value object to add note's tags."""

    name: str


class NoteValue(values.Value):
    """Value object to add notes."""

    text: str
    tags: list[TagValue]


class NoteOrdering(values.Value):
    """Value for ordering read notes result by fields."""

    created_at: values.OrderingType
