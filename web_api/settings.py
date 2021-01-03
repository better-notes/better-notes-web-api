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

    REDIS_ADDRESS: str = 'redis://localhost:6379'

    MAX_PAGING_LIMIT: int = 20
