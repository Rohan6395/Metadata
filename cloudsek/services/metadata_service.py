from datetime import datetime
from cloudsek.db.mongo import metadata_collection
from cloudsek.services.fetcher import fetch_metadata

async def create_metadata(url: str):
    existing = await metadata_collection.find_one({"url": url})
    if existing:
        return existing

    data = await fetch_metadata(url)

    document = {
        "url": url,
        "headers": data["headers"],
        "cookies": data["cookies"],
        "page_source": data["page_source"],
        "created_at": datetime.utcnow()
    }

    await metadata_collection.insert_one(document)
    return document


async def get_metadata(url: str):
    return await metadata_collection.find_one({"url": url})