from pydantic import BaseSettings
import logging


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s - %(name)s - %(levelname)s]: %(message)s',
)


class Settings(BaseSettings):
    REPOSITORY_DEFAULT_PAGE_SIZE: int = 10

    MONGO_HOST: str = 'localhost'
    MONGO_PORT: int = 27017
    MONGO_DATABASE: str = 'better_notes'
