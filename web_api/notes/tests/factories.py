import factory

from web_api import commons
from web_api.commons.tests.factories import MotorClientFactory, SettingsFactory
from web_api.notes import usecases, repositories, values


class TagValueFactory(factory.Factory):  # type: ignore
    class Meta:
        model = values.TagValue

    name = factory.Sequence('tag #{0}'.format)


class NoteValueFactory(factory.Factory):  # type: ignore
    class Meta:
        model = values.NoteValue

    text = 'Sample text'
    tags = factory.List([factory.SubFactory(TagValueFactory)])


class NoteRepositoryFactory(factory.Factory):  # type: ignore
    class Meta:
        model = repositories.NoteRepository

    client = factory.SubFactory(MotorClientFactory)
    settings = factory.SubFactory(SettingsFactory)


class NoteInteractorFactory(factory.Factory):
    class Meta:
        model = usecases.NoteInteractor

    note_repository = factory.SubFactory(NoteRepositoryFactory)


class PagingFactory(factory.Factory):
    class Meta:
        model = commons.values.Paging

    limit = 10
    offset = 0
