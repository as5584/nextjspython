from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    job_text: str = Field(..., min_length=1)


class MatchResponse(BaseModel):
    resume_keywords: list[str]
    job_keywords: list[str]
    matched: list[str]
    missing: list[str]
    extra: list[str]
    match_count: int
    total_job: int
    percentage: float
