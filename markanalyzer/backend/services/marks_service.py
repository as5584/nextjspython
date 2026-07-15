from repositories.marks_repository import MarksRepository


class MarksService:
    def __init__(self, repo: MarksRepository | None = None) -> None:
        self.repo = repo or MarksRepository()

    def _enrich(self, s: dict) -> dict:
        avg = round((s["math"] + s["science"] + s["english"]) / 3, 2)
        status = "Pass" if avg >= 40 and min(s["math"], s["science"], s["english"]) >= 40 else "Fail"
        return {**s, "average": avg, "status": status}

    def list_students(self) -> list[dict]:
        return [self._enrich(s) for s in self.repo.get_all()]

    def add_student(self, payload: dict) -> tuple[dict | None, str | None]:
        existing = self.repo.get_all()
        if any(s["roll"] == payload["roll"] for s in existing):
            return None, "Roll number already exists."
        for subject in ("math", "science", "english"):
            score = payload.get(subject, 0)
            if score < 0 or score > 100:
                return None, f"{subject} must be between 0 and 100."
        if not str(payload.get("name", "")).strip():
            return None, "Name is required."
        self.repo.add(payload)
        return self._enrich(payload), None

    def analyze(self) -> dict:
        students = self.list_students()
        if not students:
            return {
                "students": [],
                "class_average": 0.0,
                "topper": None,
                "failed": [],
            }
        class_avg = round(sum(s["average"] for s in students) / len(students), 2)
        topper = max(students, key=lambda s: s["average"])
        failed = [
            s
            for s in students
            if s["math"] < 40 or s["science"] < 40 or s["english"] < 40 or s["status"] == "Fail"
        ]
        self.repo.save_report(students)
        return {
            "students": students,
            "class_average": class_avg,
            "topper": topper,
            "failed": failed,
        }
