from pydantic import BaseSettings
import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(name)s - %(levelname)s]: %(message)s',
)


class Settings(BaseSettings):
    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = 27017
    MONGO_DATABASE: str = 'better_notes'

    MAX_PAGING_LIMIT: int = 20
