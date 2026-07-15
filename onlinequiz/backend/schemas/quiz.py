from pydantic import BaseModel, Field


class QuestionPublic(BaseModel):
    id: int
    question: str
    options: list[str]


class QuizStartResponse(BaseModel):
    session_id: str
    total: int
    time_per_question: int
    questions: list[QuestionPublic]


class AnswerSubmit(BaseModel):
    session_id: str
    question_id: int
    answer: str = Field(..., min_length=1)


class AnswerResult(BaseModel):
    correct: bool
    correct_answer: str
    current_score: int


class QuizFinishRequest(BaseModel):
    session_id: str


class QuizResult(BaseModel):
    score: int
    total: int
    percentage: float
    high_score: int
    is_new_high_score: bool
