from motor import motor_asyncio


async def create_username_unique_index(
    users_collection: motor_asyncio.AsyncIOMotorCollection,
) -> None:
    await users_collection.create_index('username', unique=True)
