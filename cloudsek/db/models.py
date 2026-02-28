from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Dict, Any

class MetadataModel(BaseModel):
    url: HttpUrl
    headers: Dict[str, Any]
    cookies: Dict[str, Any]
    page_source: str
    created_at: datetime