"""Integration tests for the API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from main import app

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_post_metadata_success():
    """Test POST /metadata creates metadata for valid URL."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/metadata", json={"url": "https://example.com"})
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert "message" in data
    assert data["message"] == "Metadata stored"


async def test_post_metadata_invalid_url_format():
    """Test POST /metadata returns 422 for invalid URL format."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/metadata", json={"url": "not-a-valid-url"})
    
    assert response.status_code == 422


async def test_post_metadata_unreachable_host():
    """Test POST /metadata returns 404 for unreachable host."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/metadata", json={"url": "https://thisdomaindoesnotexist12345.com"})
    
    assert response.status_code == 404


async def test_get_metadata_exists():
    """Test GET /metadata returns data when URL exists in DB."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # First create metadata
        await ac.post("/metadata", json={"url": "https://example.com"})
        
        # Then retrieve it
        response = await ac.get("/metadata", params={"url": "https://example.com"})
    
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert "headers" in data


async def test_get_metadata_triggers_background_collection():
    """Test GET /metadata returns 202 for valid URL not in DB."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/metadata", params={"url": "https://httpbin.org/get"})
    
    assert response.status_code in [200, 202]


async def test_get_metadata_invalid_url():
    """Test GET /metadata returns 422 for invalid URL format."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/metadata", params={"url": "invalid-url"})
    
    assert response.status_code == 422


async def test_get_metadata_unreachable_host():
    """Test GET /metadata returns 404 for unreachable host."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/metadata", params={"url": "https://thisdomaindoesnotexist12345.com"})
    
    assert response.status_code == 404
