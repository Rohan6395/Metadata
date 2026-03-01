import httpx
from typing import Dict, Any


async def fetch_metadata(url: str) -> Dict[str, Any]:
    """Fetch headers, cookies, and page source from a URL."""
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, verify=False) as client:
            response = await client.get(url)
            return {
                "headers": dict(response.headers),
                "cookies": dict(response.cookies),
                "page_source": response.text
            }
    except httpx.TimeoutException:
        raise Exception(f"Timeout while fetching {url}")
    except httpx.RequestError as e:
        raise Exception(f"Error fetching {url}: {str(e)}")