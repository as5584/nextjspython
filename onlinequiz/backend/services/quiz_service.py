import random

from repositories.quiz_repository import QuizRepository


class QuizService:
    TIME_PER_QUESTION = 30

    def __init__(self, repo: QuizRepository | None = None) -> None:
        self.repo = repo or QuizRepository()

    def start_quiz(self) -> dict:
        questions = self.repo.get_questions()
        random.shuffle(questions)
        session_id = self.repo.create_session([q["id"] for q in questions])
        public = [
            {"id": q["id"], "question": q["question"], "options": q["options"]}
            for q in questions
        ]
        return {
            "session_id": session_id,
            "total": len(public),
            "time_per_question": self.TIME_PER_QUESTION,
            "questions": public,
        }

    def submit_answer(self, session_id: str, question_id: int, answer: str) -> tuple[dict | None, str | None]:
        session = self.repo.get_session(session_id)
        if not session:
            return None, "Invalid session."
        if question_id in session["answered"]:
            return None, "Question already answered."
        all_q = {q["id"]: q for q in self.repo.get_questions()}
        q = all_q.get(question_id)
        if not q:
            return None, "Question not found."
        correct = answer == q["answer"]
        if correct:
            session["score"] += 1
        session["answered"].append(question_id)
        self.repo.update_session(session_id, session)
        return {
            "correct": correct,
            "correct_answer": q["answer"],
            "current_score": session["score"],
        }, None

    def finish(self, session_id: str) -> tuple[dict | None, str | None]:
        session = self.repo.get_session(session_id)
        if not session:
            return None, "Invalid session."
        total = len(session["question_ids"])
        score = session["score"]
        high = self.repo.get_high_score()
        is_new = score > high
        if is_new:
            self.repo.set_high_score(score)
            high = score
        return {
            "score": score,
            "total": total,
            "percentage": round((score / total) * 100, 1) if total else 0.0,
            "high_score": high,
            "is_new_high_score": is_new,
        }, None

    def high_score(self) -> int:
        return self.repo.get_high_score()
