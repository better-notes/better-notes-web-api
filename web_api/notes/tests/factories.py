import asyncio

import factory
from motor import motor_asyncio
from web_api import commons, settings
from web_api.notes import interactors, repositories, values


class TagValueFactory(factory.Factory):  # type: ignore
    class Meta:
        model = values.TagValue

    name = factory.Sequence('tag #{0}'.format)


class NoteValueFactory(factory.Factory):  # type: ignore
    class Meta:
        model = values.NoteValue

    text = 'Sample text'
    tags = factory.List([factory.SubFactory(TagValueFactory)])


class SettingsFactory(factory.Factory):  # type: ignore
    class Meta:
        model = settings.Settings


class MotorClientFactory(factory.Factory):  # type: ignore
    class Meta:
        model = motor_asyncio.AsyncIOMotorClient

    host = 'localhost'
    port = 27017
    io_loop = factory.LazyFunction(asyncio.get_event_loop)


class NoteRepositoryFactory(factory.Factory):  # type: ignore
    class Meta:
        model = repositories.NoteRepository

    client = factory.SubFactory(MotorClientFactory)
    settings = factory.SubFactory(SettingsFactory)


class NoteInteractorFactory(factory.Factory):
    class Meta:
        model = interactors.NoteInteractor

    note_repository = factory.SubFactory(NoteRepositoryFactory)


class PagingFactory(factory.Factory):
    class Meta:
        model = commons.values.Paging

    limit = 10
    offset = 0
