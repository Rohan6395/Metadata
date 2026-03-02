import pytest
from unittest.mock import AsyncMock, patch
import httpx
from cloudsek.services.fetcher import (
    fetch_metadata,
    validate_url_reachable,
    URLFetchError,
    URLNotFoundError
)

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_fetch_metadata_success():
    mock_response = AsyncMock()
    mock_response.headers = {"content-type": "text/html"}
    mock_response.cookies = {}
    mock_response.text = "<html></html>"

    with patch("cloudsek.services.fetcher.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.get.return_value = mock_response
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

        result = await fetch_metadata("https://example.com")

        assert result["headers"] == {"content-type": "text/html"}
        assert result["cookies"] == {}
        assert result["page_source"] == "<html></html>"


async def test_fetch_metadata_timeout():
    with patch("cloudsek.services.fetcher.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.get.side_effect = httpx.TimeoutException("timeout")
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

        with pytest.raises(URLFetchError, match="Timeout"):
            await fetch_metadata("https://example.com")


async def test_fetch_metadata_connection_error():            
    """Test fetch raises URLNotFoundError on connection failure."""
    with patch("cloudsek.services.fetcher.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.get.side_effect = httpx.ConnectError("connection failed")
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

        with pytest.raises(URLNotFoundError, match="Host not found"):
            await fetch_metadata("https://invalid.com")


async def test_validate_url_reachable_success():
    """Test URL validation passes for reachable URL."""
    with patch("cloudsek.services.fetcher.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.head.return_value = AsyncMock()
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

       
        await validate_url_reachable("https://example.com")


async def test_validate_url_reachable_not_found():
    with patch("cloudsek.services.fetcher.httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.head.side_effect = httpx.ConnectError("connection failed")
        mock_instance.__aenter__.return_value = mock_instance
        mock_instance.__aexit__.return_value = None
        mock_client.return_value = mock_instance

        with pytest.raises(URLNotFoundError):
            await validate_url_reachable("https://invalid.com")
