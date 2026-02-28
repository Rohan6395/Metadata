from motor.motor_asyncio import AsyncIOMotorClient
from cloudsek.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.DB_NAME]

metadata_collection = db["metadata"]