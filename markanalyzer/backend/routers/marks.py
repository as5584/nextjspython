from fastapi import APIRouter, HTTPException

from schemas.marks import AnalysisResponse, StudentCreate, StudentReport
from services.marks_service import MarksService

router = APIRouter(prefix="/marks", tags=["marks"])


@router.get("/students", response_model=list[StudentReport])
def list_students():
    return MarksService().list_students()


@router.post("/students", response_model=StudentReport, status_code=201)
def add_student(payload: StudentCreate):
    row, err = MarksService().add_student(payload.model_dump())
    if err:
        raise HTTPException(status_code=400, detail=err)
    return row


@router.get("/analysis", response_model=AnalysisResponse)
def analysis():
    return MarksService().analyze()
