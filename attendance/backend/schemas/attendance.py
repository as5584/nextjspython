from pydantic import BaseModel, Field


class AttendanceMark(BaseModel):
    student: str
    status: str = Field(..., pattern="^(P|A)$")


class AttendanceCreate(BaseModel):
    date: str | None = None
    marks: list[AttendanceMark]


class AttendanceRecordResponse(BaseModel):
    date: str
    attendance: dict[str, str]


class StudentSummary(BaseModel):
    student: str
    total_days: int
    present: int
    percentage: float


class SummaryResponse(BaseModel):
    students: list[StudentSummary]


class LowAttendanceResponse(BaseModel):
    threshold: float
    students: list[StudentSummary]
