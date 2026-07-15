from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1)


class StudentResponse(BaseModel):
    name: str
