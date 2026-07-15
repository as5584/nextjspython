import re

from repositories.resume_repository import ResumeRepository


class ResumeService:
    def __init__(self, repo: ResumeRepository | None = None) -> None:
        self.repo = repo or ResumeRepository()

    @staticmethod
    def extract_keywords(text: str) -> set[str]:
        words = re.findall(r"[A-Za-z0-9+#]+", text)
        return {word.lower() for word in words if len(word) > 1}

    def check_match(self, resume_text: str, job_text: str) -> dict:
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = self.extract_keywords(job_text)
        matched = resume_keywords & job_keywords
        missing = job_keywords - resume_keywords
        extra = resume_keywords - job_keywords
        total_job = len(job_keywords)
        match_count = len(matched)
        percentage = round((match_count / total_job) * 100, 1) if total_job > 0 else 0.0
        result = {
            "resume_keywords": sorted(resume_keywords),
            "job_keywords": sorted(job_keywords),
            "matched": sorted(matched),
            "missing": sorted(missing),
            "extra": sorted(extra),
            "match_count": match_count,
            "total_job": total_job,
            "percentage": percentage,
        }
        report = (
            "RESUME KEYWORD CHECKER REPORT\n\n"
            f"Matched: {', '.join(result['matched']) or 'None'}\n"
            f"Missing: {', '.join(result['missing']) or 'None'}\n"
            f"Match: {percentage}%\n"
        )
        self.repo.save_report(report)
        return result

    def check_from_files(self) -> tuple[dict | None, str | None]:
        try:
            resume = self.repo.read_text(self.repo.DEFAULT_RESUME)
            job = self.repo.read_text(self.repo.DEFAULT_JOB)
        except FileNotFoundError as e:
            return None, str(e)
        return self.check_match(resume, job), None
