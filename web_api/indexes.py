import asyncio

from motor import motor_asyncio

from web_api.accounts.indexes import create_username_unique_index
from web_api.settings import Settings


async def create_indexes(
    db: motor_asyncio.AsyncIOMotorDatabase, settings: Settings,
) -> None:
    await create_username_unique_index(
        users_collection=db[settings.USERS_COLLECTION],
    )


async def main():
    settings = Settings()
    motor_client = motor_asyncio.AsyncIOMotorClient(
        settings.MONGO_HOST, settings.MONGO_PORT,
    )

    await create_indexes(
        db=motor_client[settings.MONGO_DATABASE], settings=settings,
    )


if __name__ == '__main__':
    asyncio.run(main())
