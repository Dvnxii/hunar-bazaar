"""
Async MongoDB connection (Motor). Call connect_to_mongo() on startup and
close_mongo_connection() on shutdown (wired in main.py's lifespan).
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient | None = None


def get_database():
    if client is None:
        raise RuntimeError("Mongo client not initialised - call connect_to_mongo() first")
    return client[settings.mongo_db_name]


async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(settings.mongo_uri)
    # Indexes that matter for the app's access patterns
    db = get_database()
    await db.users.create_index("email", unique=True)
    await db.products.create_index("seller_id")
    await db.orders.create_index("buyer_id")
    await db.orders.create_index("delivery_agent_id")


async def close_mongo_connection():
    global client
    if client is not None:
        client.close()
        client = None
