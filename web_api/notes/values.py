from web_api.commons import values


class TagValue(values.Value):
    name: str


class NoteValue(values.Value):
    text: str
    tags: list[TagValue]
