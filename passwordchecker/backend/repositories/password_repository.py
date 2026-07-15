"""Stateless checker — repository kept for industrial layering consistency."""


class PasswordRepository:
    STRENGTH_LABELS = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Medium",
        4: "Strong",
        5: "Very Strong",
    }
