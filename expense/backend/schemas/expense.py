from pydantic import BaseModel, Field


CATEGORIES = ["FOOD", "CLOTHES", "VEHICLES", "ELECTRONICS"]
PAYMENT_METHODS = ["Online", "Cash"]


class ExpenseCreate(BaseModel):
    category: str
    item: str = Field(..., min_length=1)
    amount: float = Field(..., ge=0)
    payment_method: str
    date: str | None = None


class ExpenseResponse(BaseModel):
    id: int
    date: str
    category: str
    item: str
    amount: float
    payment_method: str


class TotalResponse(BaseModel):
    total: float


class CategoryTotal(BaseModel):
    category: str
    amount: float


class MonthlyTotal(BaseModel):
    month: str
    amount: float


class AnalyticsResponse(BaseModel):
    total: float
    by_category: list[CategoryTotal]
    by_month: list[MonthlyTotal]
    highest_category: CategoryTotal | None
