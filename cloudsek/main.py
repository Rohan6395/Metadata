from fastapi import FastAPI
from cloudsek.api.routes import router
from cloudsek.db.mongo import metadata_collection

app = FastAPI(title="HTTP Metadata Inventory Service")

@app.on_event("startup")
async def startup():
    await metadata_collection.create_index("url", unique=True)

app.include_router(router)