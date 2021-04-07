from fastapi import Depends
from motor import motor_asyncio

from web_api.commons.dependencies import (
    MONGO_CLIENT_DEPENDENCY,
    SETTINGS_DEPENDENCY,
)
from web_api.notes import usecases, repositories
from web_api.settings import Settings


def _get_note_repository(
    client: motor_asyncio.AsyncIOMotorClient = MONGO_CLIENT_DEPENDENCY,
    settings: Settings = SETTINGS_DEPENDENCY,
) -> repositories.NoteRepository:
    return repositories.NoteRepository(client=client, settings=settings)


NOTE_REPOSITORY_DEPENDENCY = Depends(_get_note_repository)


def _get_note_interactor(
    note_repository: repositories.NoteRepository = NOTE_REPOSITORY_DEPENDENCY,
) -> usecases.NoteInteractor:
    return usecases.NoteInteractor(note_repository=note_repository)


NOTE_INTERACTOR_DEPENDENCY = Depends(_get_note_interactor)
