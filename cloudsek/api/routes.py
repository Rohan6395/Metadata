from fastapi import APIRouter, status, Response, HTTPException, Query
from pydantic import HttpUrl
from cloudsek.schemas.metadata_schema import URLRequest, MetadataResponse, MessageResponse
from cloudsek.services.metadata_service import create_metadata, get_metadata
from cloudsek.services.fetcher import URLFetchError, URLNotFoundError, validate_url_reachable
from cloudsek.workers.background_worker import trigger_background_collection
from typing import Union

router = APIRouter()


@router.post("/metadata", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def post_metadata(request: URLRequest) -> MessageResponse:
    """Create a metadata record for a given URL."""
    try:
        result = await create_metadata(str(request.url))
        return MessageResponse(message="Metadata stored", data=result)
    except URLNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except URLFetchError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/metadata", response_model=Union[MetadataResponse, MessageResponse])
async def retrieve_metadata(
    url: HttpUrl = Query(..., description="URL to retrieve metadata for"),
    response: Response = None
) -> Union[MetadataResponse, MessageResponse]:
    """Retrieve metadata for a given URL. Returns 202 if not found and collection is initiated."""
    url_str = str(url)
    
    metadata = await get_metadata(url_str)
    if metadata:
        return metadata

    # Validate URL is reachable before accepting for background collection
    try:
        await validate_url_reachable(url_str)
    except URLNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except URLFetchError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    trigger_background_collection(url_str)
    response.status_code = status.HTTP_202_ACCEPTED
    return MessageResponse(message="Metadata collection initiated")