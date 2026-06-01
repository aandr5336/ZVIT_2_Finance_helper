from src.storage import (
    get_budgets as store_get, set_budget as store_set,
    delete_budget as store_delete, get_categories, get_transactions, Session,
)


def set_budget(category_id: int, amount: float, month: str) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    if amount <= 0:
        return False, "Сума має бути більше нуля"
    store_set(Session.user_id(), category_id, amount, month)
    return True, "Бюджет збережено"


def delete_budget(budget_id: int) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    store_delete(Session.user_id(), budget_id)
    return True, "Бюджет видалено"


def get_budgets_with_progress(month: str) -> list:
    if not Session.is_logged_in():
        return []

    uid = Session.user_id()
    cats = {c["id"]: c for c in get_categories(uid)}
    budgets = [b for b in store_get(uid) if b["month"] == month]
    txs = [r for r in get_transactions(uid) if r["type"] == "expense" and r["created_at"][:7] == month]

    result = []
    for b in budgets:
        cat = cats.get(b["category_id"], {"name": "Інше", "icon": "category", "color": "#888"})
        spent = sum(r["amount"] for r in txs if r.get("category_id") == b["category_id"])
        budget = b["amount"]
        percent = min(spent / budget, 1.0) if budget > 0 else 0
        result.append({
            **b,
            "category":  cat["name"],
            "icon":      cat["icon"],
            "color":     cat["color"],
            "spent":     spent,
            "percent":   percent,
            "remaining": max(budget - spent, 0),
            "is_over":   spent > budget,
        })
    return sorted(result, key=lambda x: x["spent"], reverse=True)


def get_total_budget_progress(month: str) -> dict:
    budgets = get_budgets_with_progress(month)
    total_budget = sum(b["amount"] for b in budgets)
    total_spent = sum(b["spent"] for b in budgets)
    return {
        "total_budget": total_budget,
        "total_spent":  total_spent,
        "percent":      min(total_spent / total_budget, 1.0) if total_budget > 0 else 0,
        "remaining":    max(total_budget - total_spent, 0),
    }
