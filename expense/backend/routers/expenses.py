from fastapi import APIRouter, HTTPException, Query

from schemas.expense import (
    AnalyticsResponse,
    CATEGORIES,
    ExpenseCreate,
    ExpenseResponse,
    PAYMENT_METHODS,
    TotalResponse,
)
from services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/meta")
def meta():
    return {"categories": CATEGORIES, "payment_methods": PAYMENT_METHODS}


@router.get("", response_model=list[ExpenseResponse])
@router.get("/", response_model=list[ExpenseResponse], include_in_schema=False)
def list_expenses(
    category: str | None = None,
    date: str | None = Query(None, description="YYYY-MM-DD"),
):
    return ExpenseService().list_expenses(category=category, on_date=date)


@router.post("", response_model=ExpenseResponse, status_code=201)
@router.post("/", response_model=ExpenseResponse, status_code=201, include_in_schema=False)
def add_expense(payload: ExpenseCreate):
    row, err = ExpenseService().add_expense(
        category=payload.category,
        item=payload.item,
        amount=payload.amount,
        payment_method=payload.payment_method,
        expense_date=payload.date,
    )
    if err:
        raise HTTPException(status_code=400, detail=err)
    return row


@router.get("/total", response_model=TotalResponse)
def total():
    data = ExpenseService().analytics()
    return TotalResponse(total=data["total"])


@router.get("/analytics", response_model=AnalyticsResponse)
def analytics():
    return ExpenseService().analytics()
