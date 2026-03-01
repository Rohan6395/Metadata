import pytest
from httpx import AsyncClient, ASGITransport
from main import app

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_post_metadata():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/metadata", json={"url": "https://example.com"})
    assert response.status_code in [200, 201]


async def test_get_metadata_miss():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/metadata", params={"url": "https://unknown.com"})
    assert response.status_code in [200, 202]