from pathlib import Path

from config import BASE_DIR, DATA_DIR


class ResumeRepository:
    DEFAULT_RESUME = BASE_DIR.parent / "resume.txt"
    DEFAULT_JOB = BASE_DIR.parent / "job_description.txt"

    def read_text(self, path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return path.read_text(encoding="utf-8").strip()

    def save_report(self, content: str) -> Path:
        path = DATA_DIR / "match_report.txt"
        path.write_text(content, encoding="utf-8")
        return path
