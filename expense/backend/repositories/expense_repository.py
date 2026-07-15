import csv
from pathlib import Path

from config import DATA_DIR

COLUMNS = ["Date", "Category", "Item", "Amount", "Payment Method"]


class ExpenseRepository:
    def __init__(self, data_file: Path | None = None) -> None:
        self.data_file = data_file or (DATA_DIR / "expense_tracker.csv")
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            with open(self.data_file, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(COLUMNS)

    @staticmethod
    def _pick(row: dict, *keys: str) -> str | None:
        lower_map = {
            str(k).lower().strip(): ("" if v is None else str(v).strip())
            for k, v in row.items()
            if k is not None
        }
        for key in keys:
            value = lower_map.get(key.lower())
            if value not in (None, ""):
                return value
        return None

    def get_all(self) -> list[dict]:
        if not self.data_file.exists():
            return []
        rows: list[dict] = []
        try:
            with open(self.data_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, start=1):
                    date = self._pick(row, "Date", "date")
                    category = self._pick(row, "Category", "category")
                    item = self._pick(row, "Item", "item")
                    amount_raw = self._pick(row, "Amount", "amount")
                    payment = self._pick(
                        row, "Payment Method", "payment method", "payment_method"
                    )
                    if not date or amount_raw is None:
                        continue
                    try:
                        amount = float(amount_raw)
                    except ValueError:
                        continue
                    rows.append(
                        {
                            "id": i,
                            "date": date,
                            "category": category or "",
                            "item": item or "",
                            "amount": amount,
                            "payment_method": payment or "",
                        }
                    )
        except OSError:
            return []
        return rows

    def add(
        self,
        date: str,
        category: str,
        item: str,
        amount: float,
        payment_method: str,
    ) -> dict:
        with open(self.data_file, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([date, category, item, amount, payment_method])
        rows = self.get_all()
        return rows[-1]
