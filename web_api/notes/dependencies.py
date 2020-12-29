from fastapi import Depends
from motor import motor_asyncio  # type: ignore
from web_api.notes import interactors, repositories, validators
from web_api.settings import Settings


async def get_mongo_client(
    settings: Settings = Depends(lambda: Settings()),
) -> motor_asyncio.AsyncIOMotorClient:
    # XXX: async b/c motor client requires loop for instantiation ¯\_(ツ)_/¯
    return motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_HOST, settings.MONGO_PORT,
    )


def get_note_repository(
    client: motor_asyncio.AsyncIOMotorClient = Depends(get_mongo_client),
    settings: Settings = Depends(lambda: Settings()),
) -> repositories.NoteRepository:
    return repositories.NoteRepository(client=client, settings=settings)


def get_note_interactor(
    note_repository: repositories.NoteRepository = Depends(
        get_note_repository
    ),
) -> interactors.NoteInteractor:
    return interactors.NoteInteractor(note_repository=note_repository)


def get_paging_validator(
    settings: Settings = Depends(lambda: Settings()),
) -> validators.PagingValidator:
    return validators.PagingValidator(settings=settings)
