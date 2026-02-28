import pytest
from httpx import AsyncClient
from cloudsek.main import cloudsek

@pytest.mark.asyncio
async def test_post_metadata():
    async with AsyncClient(cloudsek=cloudsek, base_url="http://test") as ac:
        response = await ac.post("/metadata", json={"url": "https://example.com"})
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_metadata_miss():
    async with AsyncClient(cloudsek=cloudsek, base_url="http://test") as ac:
        response = await ac.get("/metadata", params={"url": "https://unknown.com"})
    assert response.status_code == 200 or response.status_code == 202