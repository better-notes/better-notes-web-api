from fastapi import Depends
from fastapi.param_functions import Query
from motor import motor_asyncio

from web_api.commons.dependencies import get_mongo_client, get_settings
from web_api.notes import repositories, usecases
from web_api.notes.values import TagValue
from web_api.settings import Settings


def get_note_repository(
    client: motor_asyncio.AsyncIOMotorClient = Depends(get_mongo_client),
    settings: Settings = Depends(get_settings),
) -> repositories.NoteRepository:
    """Get note repository."""
    return repositories.NoteRepository(client=client, settings=settings)


def get_note_interactor(
    note_repository: repositories.NoteRepository = Depends(get_note_repository),
) -> usecases.NoteInteractor:
    """Get note interactor."""
    return usecases.NoteInteractor(note_repository=note_repository)


def get_tag_value_list(tags: list[str] = Query([], alias='tag')) -> list[TagValue]:
    """Get tag values from query params."""
    tag_value_list = []
    for tag in tags:
        tag_value_list.append(TagValue(name=tag))

    return tag_value_list


def get_add_welcome_note_usecase(
    note_repository: repositories.NoteRepository = Depends(get_note_repository),
) -> usecases.AddWelcomeNoteUsecase:
    """Get add welcome note usecase."""
    return usecases.AddWelcomeNoteUsecase(note_repository=note_repository)
