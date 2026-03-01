import httpx
from typing import Dict, Any


class URLFetchError(Exception):
    """Base error for URL fetching failures."""
    pass


class URLNotFoundError(URLFetchError):
    """Raised when the target host/domain cannot be reached or resolved."""
    pass


async def validate_url_reachable(url: str) -> None:
    """Quick check if URL is reachable. Raises URLNotFoundError or URLFetchError if not."""
    try:
        async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
            await client.head(url)
    except httpx.ConnectError:
        raise URLNotFoundError("Host not found or unreachable")
    except httpx.TimeoutException:
        raise URLFetchError("Timeout: URL took too long to respond")
    except httpx.RequestError as e:
        raise URLFetchError(f"Request failed: {str(e)}")


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
        raise URLFetchError("Timeout: URL took too long to respond")
    except httpx.ConnectError:
        raise URLNotFoundError("Host not found or unreachable")
    except httpx.RequestError as e:
        raise URLFetchError(f"Request failed: {str(e)}")