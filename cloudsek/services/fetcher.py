import httpx

async def fetch_metadata(url: str):
    async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
        response = await client.get(url)
        return {
            "headers": dict(response.headers),
            "cookies": dict(response.cookies),
            "page_source": response.text
        }