from contextlib import asynccontextmanager
from fastapi import FastAPI
from cloudsek.api.routes import router
from cloudsek.db.mongo import metadata_collection


@asynccontextmanager
async def lifespan(app: FastAPI):
    await metadata_collection.create_index("url", unique=True)
    yield


app = FastAPI(title="HTTP Metadata Inventory Service", lifespan=lifespan)
app.include_router(router)