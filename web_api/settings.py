import logging

from pydantic import BaseSettings

logging.basicConfig(
    level=logging.INFO,
    format='[{asctime} - {name} - {levelname}]: {message}',
    style='{',
)


class Settings(BaseSettings):
    """Project settings container."""

    mongo_host: str = 'localhost'
    mongo_port: int = 27017
    mongo_database: str = 'better_notes'

    redis_address: str = 'redis://localhost:6379'

    notes_collection: str = 'notes'
    accounts_collection: str = 'accounts'

    app_host: str = '0.0.0.0'  # noqa: S104
    app_port: int = 8000
