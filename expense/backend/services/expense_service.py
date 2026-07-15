from collections import defaultdict
from datetime import date as date_cls

from repositories.expense_repository import ExpenseRepository
from schemas.expense import CATEGORIES, PAYMENT_METHODS


class ExpenseService:
    def __init__(self, repo: ExpenseRepository | None = None) -> None:
        self.repo = repo or ExpenseRepository()

    def list_expenses(
        self,
        category: str | None = None,
        on_date: str | None = None,
    ) -> list[dict]:
        rows = self.repo.get_all()
        if category:
            rows = [r for r in rows if r["category"].upper() == category.upper()]
        if on_date:
            rows = [r for r in rows if r["date"] == on_date]
        return rows

    def add_expense(
        self,
        category: str,
        item: str,
        amount: float,
        payment_method: str,
        expense_date: str | None = None,
    ) -> tuple[dict | None, str | None]:
        category = category.upper().strip()
        if category not in CATEGORIES:
            return None, f"Category must be one of: {', '.join(CATEGORIES)}"
        item = item.strip()
        if not item or item.isdigit():
            return None, "Item name must be a non-empty text value."
        if amount < 0:
            return None, "Amount cannot be negative."
        if payment_method not in PAYMENT_METHODS:
            return None, f"Payment method must be one of: {', '.join(PAYMENT_METHODS)}"
        d = expense_date or date_cls.today().strftime("%Y-%m-%d")
        row = self.repo.add(d, category, item, amount, payment_method)
        return row, None

    def analytics(self) -> dict:
        rows = self.repo.get_all()
        total = sum(r["amount"] for r in rows)
        by_cat: dict[str, float] = defaultdict(float)
        by_month: dict[str, float] = defaultdict(float)
        for r in rows:
            by_cat[r["category"]] += r["amount"]
            by_month[r["date"][:7]] += r["amount"]
        cat_list = [{"category": k, "amount": round(v, 2)} for k, v in sorted(by_cat.items())]
        month_list = [{"month": k, "amount": round(v, 2)} for k, v in sorted(by_month.items())]
        highest = max(cat_list, key=lambda x: x["amount"]) if cat_list else None
        return {
            "total": round(total, 2),
            "by_category": cat_list,
            "by_month": month_list,
            "highest_category": highest,
        }
