import asyncio
from cloudsek.services.metadata_service import create_metadata

def trigger_background_collection(url: str):
    asyncio.create_task(create_metadata(url))