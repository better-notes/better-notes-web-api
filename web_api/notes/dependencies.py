from fastapi import Depends
from motor import motor_asyncio
from web_api.commons.dependencies import get_mongo_client
from web_api.notes import interactors, repositories
from web_api.settings import Settings


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
