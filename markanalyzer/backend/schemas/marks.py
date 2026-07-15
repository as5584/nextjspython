from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    roll: int
    name: str = Field(..., min_length=1)
    math: int = Field(..., ge=0, le=100)
    science: int = Field(..., ge=0, le=100)
    english: int = Field(..., ge=0, le=100)


class StudentReport(BaseModel):
    roll: int
    name: str
    math: int
    science: int
    english: int
    average: float
    status: str


class AnalysisResponse(BaseModel):
    students: list[StudentReport]
    class_average: float
    topper: StudentReport | None
    failed: list[StudentReport]
