from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import Dict, Optional


class URLRequest(BaseModel):
    url: HttpUrl


class MetadataResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    url: str
    headers: Dict[str, str]
    cookies: Dict[str, str]
    page_source: str
    created_at: str


class MessageResponse(BaseModel):
    message: str
    data: Optional[MetadataResponse] = None