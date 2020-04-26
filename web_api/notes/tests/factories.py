import factory

from web_api.notes import values

# Value


class TagValueFactory(factory.Factory):  # type: ignore
    class Meta:
        model = values.TagValue

    name = factory.Sequence('tag #{0}'.format)


class NoteValueFactory(factory.Factory):  # type: ignore
    class Meta:
        model = values.NoteValue

    text = 'Sample text'
    tags = factory.List([factory.SubFactory(TagValueFactory)])
