from datetime import datetime
from typing import Dict, Any, Optional
from cloudsek.db.mongo import metadata_collection
from cloudsek.services.fetcher import fetch_metadata


def serialize_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Convert MongoDB document to JSON-serializable format."""
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    if "created_at" in doc:
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


async def create_metadata(url: str) -> Dict[str, Any]:
    """Create or return existing metadata for a URL."""
    existing = await metadata_collection.find_one({"url": url})
    if existing:
        return serialize_doc(existing)

    data = await fetch_metadata(url)

    document = {
        "url": url,
        "headers": data["headers"],
        "cookies": data["cookies"],
        "page_source": data["page_source"],
        "created_at": datetime.utcnow()
    }

    result = await metadata_collection.insert_one(document)
    document["_id"] = str(result.inserted_id)
    document["created_at"] = document["created_at"].isoformat()
    return document


async def get_metadata(url: str) -> Optional[Dict[str, Any]]:
    """Get metadata for a URL if it exists."""
    doc = await metadata_collection.find_one({"url": url})
    return serialize_doc(doc)