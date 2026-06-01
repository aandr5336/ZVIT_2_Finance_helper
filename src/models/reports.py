from src.storage import Session, get_transactions as store_get_tx
from src.models.transactions import get_monthly_summary, get_expenses_by_category


def get_monthly_report(month: str) -> dict:
    summary = get_monthly_summary(month)
    by_category = get_expenses_by_category(month)
    total_expenses = summary["expenses"]
    for cat in by_category:
        cat["percent"] = round(cat["total"] / total_expenses * 100, 1) if total_expenses > 0 else 0
    return {**summary, "month": month, "by_category": by_category}


def get_last_n_months_summary(n: int = 6) -> list:
    if not Session.is_logged_in():
        return []

    rows = store_get_tx(Session.user_id())
    months = {}
    for r in rows:
        m = r["created_at"][:7]
        if m not in months:
            months[m] = {"month": m, "income": 0, "expenses": 0}
        if r["type"] == "income":
            months[m]["income"] += r["amount"]
        else:
            months[m]["expenses"] += r["amount"]

    result = sorted(months.values(), key=lambda x: x["month"])[-n:]
    for d in result:
        d["balance"] = d["income"] - d["expenses"]
    return result


def compare_months(month_a: str, month_b: str) -> dict:
    a = get_monthly_summary(month_a)
    b = get_monthly_summary(month_b)

    def diff(key):
        return round(a[key] - b[key], 2)

    def pct(key):
        if b[key] == 0:
            return None
        return round((a[key] - b[key]) / b[key] * 100, 1)

    return {
        "month_a": month_a, "month_b": month_b,
        "income_diff": diff("income"), "expenses_diff": diff("expenses"),
        "balance_diff": diff("balance"),
        "income_pct": pct("income"), "expenses_pct": pct("expenses"),
        "a": a, "b": b,
    }


def get_savings_rate(month: str) -> float:
    s = get_monthly_summary(month)
    if s["income"] == 0:
        return 0.0
    return round(s["balance"] / s["income"] * 100, 1)
