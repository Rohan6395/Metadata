from fastapi import APIRouter, status, Response
from cloudsek.schemas.metadata_schema import URLRequest
from cloudsek.services.metadata_service import create_metadata, get_metadata
from cloudsek.workers.background_worker import trigger_background_collection
from fastapi import HTTPException

router = APIRouter()



@router.post("/metadata", status_code=status.HTTP_201_CREATED)
async def post_metadata(request: URLRequest):
    try:
        result = await create_metadata(str(request.url))
        return {"message": "Metadata stored", "data": result}
    except Exception as e:
        # For debugging only
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metadata")
async def retrieve_metadata(url: str, response: Response):
    metadata = await get_metadata(url)

    if metadata:
        return metadata

    trigger_background_collection(url)
    response.status_code = status.HTTP_202_ACCEPTED
    return {"message": "Metadata collection initiated"}