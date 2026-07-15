import json
import uuid
from pathlib import Path

from config import DATA_DIR

QUESTIONS = [
    {
        "id": 1,
        "question": "What is the correct file extension for Python files?",
        "options": [".py", ".pt", ".pyt", ".p"],
        "answer": ".py",
    },
    {
        "id": 2,
        "question": "How do you create a variable with the numeric value 5?",
        "options": ["x = int(5)", "x = 5", "int x = 5", "x <- 5"],
        "answer": "x = 5",
    },
    {
        "id": 3,
        "question": "Which of the following is a correct syntax to output 'Hello World' in Python?",
        "options": [
            "echo 'Hello World'",
            "print('Hello World')",
            "p('Hello World')",
            "printf('Hello World')",
        ],
        "answer": "print('Hello World')",
    },
    {
        "id": 4,
        "question": "What is the correct way to create a function in Python?",
        "options": [
            "function myFunction():",
            "create myFunction():",
            "def myFunction():",
            "myFunction():",
        ],
        "answer": "def myFunction():",
    },
    {
        "id": 5,
        "question": "Which method can be used to remove any whitespace from both the beginning and the end of a string?",
        "options": ["strip()", "trim()", "stripped()", "len()"],
        "answer": "strip()",
    },
    {
        "id": 6,
        "question": "Which of the following statements is used to create an empty set?",
        "options": ["set = {}", "set = []", "set = set()", "set = ()"],
        "answer": "set = set()",
    },
    {
        "id": 7,
        "question": "Which operator is used to multiply numbers in Python?",
        "options": ["%", "*", "#", "&"],
        "answer": "*",
    },
    {
        "id": 8,
        "question": "How do you insert COMMENTS in Python code?",
        "options": [
            "/* This is a comment */",
            "// This is a comment",
            "# This is a comment",
            "-- This is a comment",
        ],
        "answer": "# This is a comment",
    },
    {
        "id": 9,
        "question": "What is the correct way to write a list in Python?",
        "options": ["{1, 2, 3}", "[1, 2, 3]", "(1, 2, 3)", "<1, 2, 3>"],
        "answer": "[1, 2, 3]",
    },
    {
        "id": 10,
        "question": "What is a correct syntax to return the first character in a string?",
        "options": [
            "x = sub('Hello', 0, 1)",
            "x = 'Hello'.sub(0, 1)",
            "x = 'Hello'[0]",
            "x = substring('Hello', 0, 1)",
        ],
        "answer": "x = 'Hello'[0]",
    },
]


class QuizRepository:
    def __init__(self) -> None:
        self.high_score_file = DATA_DIR / "high_score.txt"
        self.sessions_file = DATA_DIR / "sessions.json"
        DATA_DIR.mkdir(exist_ok=True)

    def get_questions(self) -> list[dict]:
        return [dict(q) for q in QUESTIONS]

    def get_high_score(self) -> int:
        if not self.high_score_file.exists():
            return 0
        try:
            raw = self.high_score_file.read_text(encoding="utf-8").strip()
            if not raw:
                return 0
            return int(raw)
        except (ValueError, OSError):
            return 0

    def set_high_score(self, score: int) -> None:
        self.high_score_file.write_text(str(score), encoding="utf-8")

    def _load_sessions(self) -> dict:
        if not self.sessions_file.exists():
            return {}
        try:
            with open(self.sessions_file, encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_sessions(self, sessions: dict) -> None:
        # Cap stored sessions so the file cannot grow forever
        if len(sessions) > 200:
            keys = list(sessions.keys())[-200:]
            sessions = {k: sessions[k] for k in keys}
        with open(self.sessions_file, "w", encoding="utf-8") as f:
            json.dump(sessions, f)

    def create_session(self, question_ids: list[int]) -> str:
        session_id = str(uuid.uuid4())
        sessions = self._load_sessions()
        sessions[session_id] = {
            "score": 0,
            "answered": [],
            "question_ids": question_ids,
        }
        self._save_sessions(sessions)
        return session_id

    def get_session(self, session_id: str) -> dict | None:
        return self._load_sessions().get(session_id)

    def update_session(self, session_id: str, data: dict) -> None:
        sessions = self._load_sessions()
        if session_id in sessions:
            sessions[session_id] = data
            self._save_sessions(sessions)
