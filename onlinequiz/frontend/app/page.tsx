"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Question = { id: number; question: string; options: string[] };
type Start = {
  session_id: string;
  total: number;
  time_per_question: number;
  questions: Question[];
};
type Finish = {
  score: number;
  total: number;
  percentage: number;
  high_score: number;
  is_new_high_score: boolean;
};

export default function HomePage() {
  const [quiz, setQuiz] = useState<Start | null>(null);
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState("");
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(30);
  const [finished, setFinished] = useState<Finish | null>(null);
  const [error, setError] = useState("");
  const [highScore, setHighScore] = useState(0);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    apiFetch<{ high_score: number }>("/quiz/high-score")
      .then((r) => {
        setHighScore(r.high_score);
        setError("");
      })
      .catch((e) => {
        setError(e instanceof Error ? e.message : "Cannot load high score");
      });
  }, []);

  useEffect(() => {
    if (!quiz || finished || busy) return;
    if (timeLeft <= 0) {
      void handleTimeout();
      return;
    }
    const t = setTimeout(() => setTimeLeft((x) => x - 1), 1000);
    return () => clearTimeout(t);
  }, [timeLeft, quiz, finished, busy]);

  async function start() {
    setError("");
    setFinished(null);
    setFeedback("");
    setSelected("");
    setIndex(0);
    setScore(0);
    try {
      const data = await apiFetch<Start>("/quiz/start", { method: "POST" });
      setQuiz(data);
      setTimeLeft(data.time_per_question);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed");
    }
  }

  async function finishQuiz(sessionId: string) {
    const res = await apiFetch<Finish>("/quiz/finish", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId }),
    });
    setFinished(res);
    setHighScore(res.high_score);
    setQuiz(null);
  }

  async function goNext(sessionId: string, nextIndex: number, total: number) {
    if (nextIndex >= total) {
      await finishQuiz(sessionId);
    } else {
      setIndex(nextIndex);
      setSelected("");
      setFeedback("");
      setTimeLeft(quiz?.time_per_question || 30);
      setBusy(false);
    }
  }

  async function submitAnswer() {
    if (!quiz || !selected || busy) return;
    setBusy(true);
    setError("");
    try {
      const q = quiz.questions[index];
      const res = await apiFetch<{
        correct: boolean;
        correct_answer: string;
        current_score: number;
      }>("/quiz/answer", {
        method: "POST",
        body: JSON.stringify({
          session_id: quiz.session_id,
          question_id: q.id,
          answer: selected,
        }),
      });
      setScore(res.current_score);
      setFeedback(
        res.correct
          ? "Correct!"
          : `Wrong. Correct answer: ${res.correct_answer}`
      );
      setTimeout(() => {
        void goNext(quiz.session_id, index + 1, quiz.total);
      }, 1200);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed");
      setBusy(false);
    }
  }

  async function handleTimeout() {
    if (!quiz || busy) return;
    setBusy(true);
    const q = quiz.questions[index];
    try {
      const res = await apiFetch<{
        correct: boolean;
        correct_answer: string;
        current_score: number;
      }>("/quiz/answer", {
        method: "POST",
        body: JSON.stringify({
          session_id: quiz.session_id,
          question_id: q.id,
          answer: "__timeout__",
        }),
      });
      setScore(res.current_score);
      setFeedback(`Time's up! Correct answer: ${res.correct_answer}`);
    } catch {
      setFeedback("Time's up!");
    }
    setTimeout(() => {
      void goNext(quiz.session_id, index + 1, quiz.total);
    }, 1500);
  }

  const current = quiz?.questions[index];

  return (
    <main>
      <div className="hero">
        <h1>Online Quiz</h1>
        <p>Python quiz with timer · High score: {highScore}</p>
      </div>
      {error && (
        <div className="error" style={{ whiteSpace: "pre-wrap" }}>
          {error}
        </div>
      )}

      {!quiz && !finished && (
        <div className="card">
          <p className="muted">10 questions · 30 seconds each</p>
          <button onClick={start} style={{ marginTop: 12 }}>
            Start quiz
          </button>
        </div>
      )}

      {finished && (
        <div className="card">
          <p className="stat">
            {finished.score}/{finished.total} ({finished.percentage}%)
          </p>
          <p>
            High score: {finished.high_score}
            {finished.is_new_high_score ? " · New high score!" : ""}
          </p>
          <button onClick={start} style={{ marginTop: 12 }}>
            Play again
          </button>
        </div>
      )}

      {quiz && current && (
        <div className="card">
          <div className="row">
            <span className="pill">
              Question {index + 1}/{quiz.total}
            </span>
            <span className="pill">Score: {score}</span>
            <span className="pill">⏱ {timeLeft}s</span>
          </div>
          <h3 style={{ marginTop: 16 }}>{current.question}</h3>
          <div className="options" style={{ marginTop: 12 }}>
            {current.options.map((opt) => (
              <label key={opt} className="option">
                <input
                  type="radio"
                  name="answer"
                  value={opt}
                  checked={selected === opt}
                  onChange={() => setSelected(opt)}
                  disabled={busy}
                />
                {opt}
              </label>
            ))}
          </div>
          {feedback && (
            <p className={feedback.startsWith("Correct") ? "ok" : "bad"} style={{ marginTop: 12 }}>
              {feedback}
            </p>
          )}
          <button
            onClick={submitAnswer}
            disabled={!selected || busy}
            style={{ marginTop: 16 }}
          >
            Submit answer
          </button>
        </div>
      )}
    </main>
  );
}
