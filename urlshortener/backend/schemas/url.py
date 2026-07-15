from pydantic import BaseModel, Field


class ShortenRequest(BaseModel):
    url: str = Field(..., min_length=3)


class UrlEntry(BaseModel):
    id: int
    original_url: str
    short_url: str
    created_at: str


class ShortenResponse(BaseModel):
    entry: UrlEntry
