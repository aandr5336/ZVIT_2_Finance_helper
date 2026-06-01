from src.storage import (
    get_transactions as store_get, add_transaction as store_add,
    delete_transaction as store_delete, get_categories, Session,
)


def _cat_map(user_id: int) -> dict:
    return {c["id"]: c for c in get_categories(user_id)}


def add_transaction(category_id: int, amount: float, tx_type: str, note: str = "", date: str = "") -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    if amount <= 0:
        return False, "Сума має бути більше нуля"
    if tx_type not in ("expense", "income"):
        return False, "Невірний тип"

    data = {
        "category_id": category_id,
        "amount":      amount,
        "type":        tx_type,
        "note":        note.strip(),
    }
    if date:
        data["created_at"] = date + " 00:00:00"

    store_add(Session.user_id(), data)
    return True, "Транзакцію додано"


def delete_transaction(tx_id: int) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    store_delete(Session.user_id(), tx_id)
    return True, "Транзакцію видалено"


def get_transactions(tx_type=None, month=None, search="", limit=200) -> list:
    if not Session.is_logged_in():
        return []

    uid = Session.user_id()
    rows = store_get(uid)
    cats = _cat_map(uid)

    if tx_type:
        rows = [r for r in rows if r["type"] == tx_type]
    if month:
        rows = [r for r in rows if r["created_at"][:7] == month]
    if search:
        s = search.lower()
        rows = [r for r in rows if s in r.get("note", "").lower() or
                s in cats.get(r.get("category_id"), {}).get("name", "").lower()]

    rows = sorted(rows, key=lambda r: r["created_at"], reverse=True)[:limit]

    result = []
    for r in rows:
        cat = cats.get(r.get("category_id"), {"name": "Без категорії", "icon": "category", "color": "#888"})
        result.append({**r, "category": cat["name"], "icon": cat["icon"], "color": cat["color"]})
    return result


def get_monthly_summary(month: str) -> dict:
    if not Session.is_logged_in():
        return {"income": 0, "expenses": 0, "balance": 0}

    rows = [r for r in store_get(Session.user_id()) if r["created_at"][:7] == month]
    income = sum(r["amount"] for r in rows if r["type"] == "income")
    expenses = sum(r["amount"] for r in rows if r["type"] == "expense")
    return {"income": income, "expenses": expenses, "balance": income - expenses}


def get_expenses_by_category(month: str) -> list:
    if not Session.is_logged_in():
        return []

    uid = Session.user_id()
    cats = _cat_map(uid)
    rows = [r for r in store_get(uid) if r["type"] == "expense" and r["created_at"][:7] == month]

    grouped = {}
    for r in rows:
        cid = r.get("category_id") or 0
        if cid not in grouped:
            cat = cats.get(cid, {"name": "Інше", "icon": "category", "color": "#888"})
            grouped[cid] = {"name": cat["name"], "icon": cat["icon"], "color": cat["color"], "total": 0, "count": 0}
        grouped[cid]["total"] += r["amount"]
        grouped[cid]["count"] += 1

    return sorted(grouped.values(), key=lambda x: x["total"], reverse=True)
