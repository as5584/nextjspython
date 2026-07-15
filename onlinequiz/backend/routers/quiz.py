from fastapi import APIRouter, HTTPException

from schemas.quiz import (
    AnswerResult,
    AnswerSubmit,
    QuizFinishRequest,
    QuizResult,
    QuizStartResponse,
)
from services.quiz_service import QuizService

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/start", response_model=QuizStartResponse)
def start_quiz():
    return QuizService().start_quiz()


@router.post("/answer", response_model=AnswerResult)
def submit_answer(payload: AnswerSubmit):
    result, err = QuizService().submit_answer(
        payload.session_id, payload.question_id, payload.answer
    )
    if err:
        raise HTTPException(status_code=400, detail=err)
    return result


@router.post("/finish", response_model=QuizResult)
def finish(payload: QuizFinishRequest):
    result, err = QuizService().finish(payload.session_id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return result


@router.get("/high-score")
def high_score():
    return {"high_score": QuizService().high_score()}
