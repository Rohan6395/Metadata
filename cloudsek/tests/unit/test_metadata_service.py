"""Unit tests for the metadata service."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
from bson import ObjectId
from cloudsek.services.metadata_service import (
    create_metadata,
    get_metadata,
    serialize_doc
)


def test_serialize_doc_none():
    """Test serialize_doc returns None for None input."""
    assert serialize_doc(None) is None


def test_serialize_doc_converts_objectid():
    """Test serialize_doc converts ObjectId to string."""
    doc = {
        "_id": ObjectId("507f1f77bcf86cd799439011"),
        "url": "https://example.com",
        "created_at": datetime(2024, 1, 1, 12, 0, 0)
    }
    result = serialize_doc(doc)
    
    assert result["_id"] == "507f1f77bcf86cd799439011"
    assert result["created_at"] == "2024-01-01T12:00:00"


pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_create_metadata_existing():
    """Test create_metadata returns existing record if found."""
    existing_doc = {
        "_id": ObjectId("507f1f77bcf86cd799439011"),
        "url": "https://example.com",
        "headers": {},
        "cookies": {},
        "page_source": "<html></html>",
        "created_at": datetime(2024, 1, 1)
    }

    with patch("cloudsek.services.metadata_service.metadata_collection") as mock_collection:
        mock_collection.find_one = AsyncMock(return_value=existing_doc)

        result = await create_metadata("https://example.com")

        assert result["url"] == "https://example.com"
        mock_collection.find_one.assert_called_once_with({"url": "https://example.com"})


async def test_create_metadata_new():
    """Test create_metadata creates new record if not found."""
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = ObjectId("507f1f77bcf86cd799439011")

    with patch("cloudsek.services.metadata_service.metadata_collection") as mock_collection:
        mock_collection.find_one = AsyncMock(return_value=None)
        mock_collection.insert_one = AsyncMock(return_value=mock_insert_result)

        with patch("cloudsek.services.metadata_service.fetch_metadata") as mock_fetch:
            mock_fetch.return_value = {
                "headers": {"content-type": "text/html"},
                "cookies": {},
                "page_source": "<html></html>"
            }

            result = await create_metadata("https://example.com")

            assert result["url"] == "https://example.com"
            assert result["headers"] == {"content-type": "text/html"}
            mock_collection.insert_one.assert_called_once()


async def test_get_metadata_found():
    """Test get_metadata returns serialized doc when found."""
    existing_doc = {
        "_id": ObjectId("507f1f77bcf86cd799439011"),
        "url": "https://example.com",
        "headers": {},
        "cookies": {},
        "page_source": "<html></html>",
        "created_at": datetime(2024, 1, 1)
    }

    with patch("cloudsek.services.metadata_service.metadata_collection") as mock_collection:
        mock_collection.find_one = AsyncMock(return_value=existing_doc)

        result = await get_metadata("https://example.com")

        assert result is not None
        assert result["url"] == "https://example.com"


async def test_get_metadata_not_found():
    """Test get_metadata returns None when not found."""
    with patch("cloudsek.services.metadata_service.metadata_collection") as mock_collection:
        mock_collection.find_one = AsyncMock(return_value=None)

        result = await get_metadata("https://notfound.com")

        assert result is None
