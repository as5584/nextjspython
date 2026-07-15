import csv
from pathlib import Path

from config import DATA_DIR


class MarksRepository:
    def __init__(self, data_file: Path | None = None) -> None:
        self.data_file = data_file or (DATA_DIR / "students.csv")
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            with open(self.data_file, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(
                    ["roll_no", "name", "math", "science", "english"]
                )

    @staticmethod
    def _pick(row: dict, *keys: str) -> str | None:
        lower_map = {str(k).lower().strip(): v for k, v in row.items() if k is not None}
        for key in keys:
            value = lower_map.get(key.lower())
            if value not in (None, ""):
                return str(value).strip()
        return None

    def get_all(self) -> list[dict]:
        if not self.data_file.exists():
            return []
        rows: list[dict] = []
        try:
            with open(self.data_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    roll = self._pick(row, "RollNo", "roll_no", "roll")
                    name = self._pick(row, "Name", "name")
                    math = self._pick(row, "Math", "math")
                    science = self._pick(row, "Science", "science")
                    english = self._pick(row, "English", "english")
                    if roll is None or name is None:
                        continue
                    try:
                        rows.append(
                            {
                                "roll": int(float(roll)),
                                "name": name,
                                "math": int(float(math or 0)),
                                "science": int(float(science or 0)),
                                "english": int(float(english or 0)),
                            }
                        )
                    except ValueError:
                        continue
        except OSError:
            return []
        return rows

    def add(self, student: dict) -> dict:
        with open(self.data_file, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(
                [
                    student["roll"],
                    student["name"],
                    student["math"],
                    student["science"],
                    student["english"],
                ]
            )
        return student

    def save_report(self, reports: list[dict]) -> Path:
        path = DATA_DIR / "report.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["RollNo", "Name", "Math", "Average", "Status"])
            for s in reports:
                writer.writerow(
                    [s["roll"], s["name"], s["math"], s["average"], s["status"]]
                )
        return path
