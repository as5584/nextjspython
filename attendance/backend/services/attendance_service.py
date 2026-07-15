from datetime import datetime

from repositories.attendance_repository import AttendanceRepository


class AttendanceService:
    def __init__(self, repo: AttendanceRepository | None = None) -> None:
        self.repo = repo or AttendanceRepository()

    def list_students(self) -> list[str]:
        students, _ = self.repo.load()
        return students

    def add_student(self, name: str) -> tuple[bool, str]:
        name = name.strip()
        if not name:
            return False, "Student name is required."
        students, records = self.repo.load()
        if name in students:
            return False, "Student already exists."
        students.append(name)
        self.repo.save(students, records)
        return True, f"Added student: {name}"

    def record_attendance(self, date: str | None, marks: list[dict]) -> tuple[bool, str]:
        students, records = self.repo.load()
        if not students:
            return False, "No students added yet."
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        attendance = {}
        for m in marks:
            student = m["student"]
            status = m["status"].upper()
            if student not in students:
                return False, f"Unknown student: {student}"
            if status not in ("P", "A"):
                return False, "Status must be P or A."
            attendance[student] = status
        for s in students:
            attendance.setdefault(s, "A")
        records.append({"date": date, "attendance": attendance})
        self.repo.save(students, records)
        return True, f"Attendance recorded for {date}"

    def list_records(self) -> list[dict]:
        _, records = self.repo.load()
        return records

    @staticmethod
    def _percentage(att_list: list[str]) -> float:
        if not att_list:
            return 0.0
        present = sum(1 for a in att_list if a == "P")
        return round((present / len(att_list)) * 100, 1)

    def summary(self) -> list[dict]:
        students, records = self.repo.load()
        result = []
        for student in students:
            att = [r["attendance"].get(student, "A") for r in records]
            present = sum(1 for x in att if x == "P")
            result.append(
                {
                    "student": student,
                    "total_days": len(att),
                    "present": present,
                    "percentage": self._percentage(att),
                }
            )
        return result

    def low_attendance(self, threshold: float = 75.0) -> list[dict]:
        return [s for s in self.summary() if s["total_days"] > 0 and s["percentage"] < threshold]
