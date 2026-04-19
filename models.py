from typing import Optional
from pydantic import BaseModel


class SubmitAnswerRequest(BaseModel):
    student_id: int
    question_id: int
    choice_given: int  # 0–3
    response_time_ms: int


class SubmitAnswerResponse(BaseModel):
    is_correct: bool
    ai_feedback: str
    next_challenge: Optional[str] = None


class StudentProgress(BaseModel):
    student_id: int
    topic: str
    avg_score: float
    avg_time_ms: int
    num_quizzes: int