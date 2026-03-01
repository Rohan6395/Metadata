import asyncio
from cloudsek.services.metadata_service import create_metadata


def trigger_background_collection(url: str) -> None:
    """Trigger background metadata collection without blocking the response."""
    loop = asyncio.get_event_loop()
    loop.create_task(create_metadata(url))