import json
from pathlib import Path

from config import DATA_DIR


class UrlRepository:
    def __init__(self, data_file: Path | None = None) -> None:
        self.data_file = data_file or (DATA_DIR / "history.json")

    def load(self) -> list[dict]:
        if not self.data_file.exists():
            return []
        with open(self.data_file, encoding="utf-8") as f:
            return json.load(f)

    def save(self, history: list[dict]) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    def add(self, entry: dict) -> list[dict]:
        history = self.load()
        history.insert(0, entry)
        self.save(history)
        return history
