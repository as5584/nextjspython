import csv
from pathlib import Path

from config import DATA_DIR


class AttendanceRepository:
    def __init__(self, data_file: Path | None = None) -> None:
        self.data_file = data_file or (DATA_DIR / "attendance_data.csv")
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> tuple[list[str], list[dict]]:
        students: list[str] = []
        records: list[dict] = []
        if not self.data_file.exists():
            return students, records

        try:
            with open(self.data_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                current_date = None
                current_att: dict[str, str] = {}
                for row in reader:
                    date = (row.get("Date") or row.get("date") or "").strip()
                    student = (row.get("Student") or row.get("student") or "").strip()
                    status = (row.get("Status") or row.get("status") or "").strip().upper()
                    if not date or not student:
                        continue
                    if status not in ("P", "A"):
                        status = "A"
                    if date != current_date and current_date is not None:
                        records.append(
                            {"date": current_date, "attendance": current_att.copy()}
                        )
                        current_att = {}
                    current_date = date
                    current_att[student] = status
                    if student not in students:
                        students.append(student)
                if current_date:
                    records.append(
                        {"date": current_date, "attendance": current_att}
                    )
        except OSError:
            return [], []
        return students, records

    def save(self, students: list[str], records: list[dict]) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Student", "Status"])
            for record in records:
                for student, status in record["attendance"].items():
                    writer.writerow([record["date"], student, status])
