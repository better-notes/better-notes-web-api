import factory

from web_api.notes import values


class TagFactory(factory.Factory):  # type: ignore
    class Meta:
        model = values.Tag

    name = factory.Sequence('tag #{0}'.format)


class NoteFactory(factory.Factory):  # type: ignore
    class Meta:
        model = values.Note

    text = 'Sample text'
    tags = factory.List([factory.SubFactory(TagFactory)])
