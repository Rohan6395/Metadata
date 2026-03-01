from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from cloudsek.api.routes import router
from cloudsek.db.mongo import metadata_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: ensure DB index exists, tolerate DB startup delays."""
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            await metadata_collection.create_index("url", unique=True)
            break
        except Exception:
            if attempt == max_retries:
                # Give up on index creation but still allow app to start
                break
            await asyncio.sleep(1)
    yield


app = FastAPI(title="HTTP Metadata Inventory Service", lifespan=lifespan)
app.include_router(router)