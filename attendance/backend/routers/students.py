from fastapi import APIRouter, HTTPException

from schemas.student import StudentCreate, StudentResponse
from services.attendance_service import AttendanceService

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentResponse])
@router.get("/", response_model=list[StudentResponse], include_in_schema=False)
def list_students():
    return [{"name": n} for n in AttendanceService().list_students()]


@router.post("", response_model=dict, status_code=201)
@router.post("/", response_model=dict, status_code=201, include_in_schema=False)
def add_student(payload: StudentCreate):
    ok, message = AttendanceService().add_student(payload.name)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message, "name": payload.name.strip()}
