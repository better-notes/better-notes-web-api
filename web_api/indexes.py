import asyncio

from motor import motor_asyncio

from web_api.accounts.indexes import create_username_unique_index
from web_api.settings import Settings


async def create_indexes(db: motor_asyncio.AsyncIOMotorDatabase, settings: Settings) -> None:
    """Create all indexes for the project."""
    await create_username_unique_index(users_collection=db[settings.accounts_collection])


async def main():
    """Prepare dependencies & create indexes."""
    settings = Settings()
    motor_client = motor_asyncio.AsyncIOMotorClient(settings.mongo_host, settings.mongo_port)

    await create_indexes(
        db=motor_client[settings.mongo_database], settings=settings,
    )


if __name__ == '__main__':
    asyncio.run(main())
