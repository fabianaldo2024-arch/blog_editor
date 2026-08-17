from pydantic import BaseModel
from datetime import datetime

class ShortLinkCreate(BaseModel):
    original_url: str

class ShortLinkResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    clicks: int
    created_at: datetime

    class Config:
        orm_mode = True
