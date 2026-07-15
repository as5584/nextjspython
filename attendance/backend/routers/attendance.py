from fastapi import APIRouter, HTTPException, Query

from schemas.attendance import (
    AttendanceCreate,
    AttendanceRecordResponse,
    LowAttendanceResponse,
    SummaryResponse,
    StudentSummary,
)
from services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("/records", response_model=list[AttendanceRecordResponse])
def list_records():
    return AttendanceService().list_records()


@router.post("/records", response_model=dict, status_code=201)
def create_record(payload: AttendanceCreate):
    marks = [m.model_dump() for m in payload.marks]
    ok, message = AttendanceService().record_attendance(payload.date, marks)
    if not ok:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}


@router.get("/summary", response_model=SummaryResponse)
def summary():
    rows = AttendanceService().summary()
    return SummaryResponse(students=[StudentSummary(**r) for r in rows])


@router.get("/low", response_model=LowAttendanceResponse)
def low_attendance(threshold: float = Query(75.0, ge=0, le=100)):
    rows = AttendanceService().low_attendance(threshold)
    return LowAttendanceResponse(
        threshold=threshold,
        students=[StudentSummary(**r) for r in rows],
    )
