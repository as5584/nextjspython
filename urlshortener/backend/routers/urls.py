from fastapi import APIRouter, HTTPException

from schemas.url import ShortenRequest, ShortenResponse, UrlEntry
from services.url_service import UrlService

router = APIRouter(prefix="/urls", tags=["urls"])


@router.get("", response_model=list[UrlEntry])
@router.get("/", response_model=list[UrlEntry], include_in_schema=False)
def history():
    return UrlService().list_history()


@router.post("/shorten", response_model=ShortenResponse, status_code=201)
def shorten(payload: ShortenRequest):
    entry, err = UrlService().shorten(payload.url)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return ShortenResponse(entry=entry)


@router.get("/{entry_id}", response_model=UrlEntry)
def get_entry(entry_id: int):
    entry = UrlService().get_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found.")
    return entry
