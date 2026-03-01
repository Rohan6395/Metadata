from fastapi import APIRouter, status, Response, HTTPException
from cloudsek.schemas.metadata_schema import URLRequest, MetadataResponse, MessageResponse
from cloudsek.services.metadata_service import create_metadata, get_metadata
from cloudsek.workers.background_worker import trigger_background_collection
from typing import Union

router = APIRouter()


@router.post("/metadata", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def post_metadata(request: URLRequest) -> MessageResponse:
    """Create a metadata record for a given URL."""
    try:
        result = await create_metadata(str(request.url))
        return MessageResponse(message="Metadata stored", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metadata", response_model=Union[MetadataResponse, MessageResponse])
async def retrieve_metadata(url: str, response: Response) -> Union[MetadataResponse, MessageResponse]:
    """Retrieve metadata for a given URL. Returns 202 if not found and collection is initiated."""
    metadata = await get_metadata(url)

    if metadata:
        return metadata

    trigger_background_collection(url)
    response.status_code = status.HTTP_202_ACCEPTED
    return MessageResponse(message="Metadata collection initiated")