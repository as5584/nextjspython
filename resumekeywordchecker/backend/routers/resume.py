from fastapi import APIRouter, HTTPException

from schemas.resume import MatchRequest, MatchResponse
from services.resume_service import ResumeService

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/match", response_model=MatchResponse)
def match(payload: MatchRequest):
    return ResumeService().check_match(payload.resume_text, payload.job_text)


@router.post("/match-files", response_model=MatchResponse)
def match_files():
    result, err = ResumeService().check_from_files()
    if err:
        raise HTTPException(status_code=400, detail=err)
    return result
