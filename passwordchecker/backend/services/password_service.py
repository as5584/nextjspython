import re

from repositories.password_repository import PasswordRepository


class PasswordService:
    def __init__(self, repo: PasswordRepository | None = None) -> None:
        self.repo = repo or PasswordRepository()

    def check(self, password: str) -> dict:
        checks = {
            "has_uppercase": bool(re.search(r"[A-Z]", password)),
            "has_lowercase": bool(re.search(r"[a-z]", password)),
            "has_numbers": bool(re.search(r"\d", password)),
            "has_symbols": bool(re.search(r"[^\w\s]", password)),
            "min_length": len(password) >= 8,
        }
        score = sum(checks.values())
        return {
            "checks": checks,
            "score": score,
            "max_score": 5,
            "percentage": round((score / 5) * 100),
            "strength": self.repo.STRENGTH_LABELS[score],
        }
