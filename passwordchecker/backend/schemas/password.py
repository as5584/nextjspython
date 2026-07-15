from pydantic import BaseModel, Field


class PasswordCheckRequest(BaseModel):
    password: str = Field(..., min_length=1)


class PasswordChecks(BaseModel):
    has_uppercase: bool
    has_lowercase: bool
    has_numbers: bool
    has_symbols: bool
    min_length: bool


class PasswordCheckResponse(BaseModel):
    checks: PasswordChecks
    score: int
    max_score: int
    percentage: int
    strength: str
