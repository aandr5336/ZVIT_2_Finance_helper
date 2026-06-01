import json
from pathlib import Path
from datetime import datetime

DATA_DIR  = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "data.json"


def _read() -> dict:
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        return {"users": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"users": []}


def _write(data: dict):
    DATA_DIR.mkdir(exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _next_id(records: list) -> int:
    return max((r["id"] for r in records), default=0) + 1


def _update_user_list(user_id: int, key: str, records: list):
    db = _read()
    for u in db["users"]:
        if u["id"] == user_id:
            u[key] = records
            _write(db)
            return



def get_all_users() -> list:
    return _read()["users"]


def get_user(user_id: int):
    return next((u for u in _read()["users"] if u["id"] == user_id), None)


def get_user_by_email(email: str):
    return next((u for u in _read()["users"] if u["email"] == email), None)


def create_user(name: str, email: str, password: str) -> dict:
    db = _read()
    user = {
        "id":           _next_id(db["users"]),
        "name":         name,
        "email":        email,
        "password":     password,
        "created_at":   _now(),
        "categories":   [],
        "transactions": [],
        "budgets":      [],
        "goals":        [],
    }
    db["users"].append(user)
    _write(db)
    return user


def update_user(user_id: int, **kwargs) -> bool:
    db = _read()
    for u in db["users"]:
        if u["id"] == user_id:
            u.update(kwargs)
            _write(db)
            return True
    return False



def get_categories(user_id: int) -> list:
    u = get_user(user_id)
    return u["categories"] if u else []


def add_category(user_id: int, data: dict) -> dict:
    cats = get_categories(user_id)
    record = {"id": _next_id(cats), "created_at": _now(), **data}
    cats.append(record)
    _update_user_list(user_id, "categories", cats)
    return record


def update_category(user_id: int, cat_id: int, **kwargs) -> bool:
    cats = get_categories(user_id)
    for c in cats:
        if c["id"] == cat_id:
            c.update(kwargs)
            _update_user_list(user_id, "categories", cats)
            return True
    return False


def delete_category(user_id: int, cat_id: int) -> bool:
    cats = get_categories(user_id)
    new = [c for c in cats if c["id"] != cat_id]
    if len(new) == len(cats):
        return False
    _update_user_list(user_id, "categories", new)
    return True



def get_transactions(user_id: int) -> list:
    u = get_user(user_id)
    return u["transactions"] if u else []


def add_transaction(user_id: int, data: dict) -> dict:
    txs = get_transactions(user_id)
    record = {"id": _next_id(txs), "created_at": _now(), **data}
    txs.append(record)
    _update_user_list(user_id, "transactions", txs)
    return record


def delete_transaction(user_id: int, tx_id: int) -> bool:
    txs = get_transactions(user_id)
    new = [t for t in txs if t["id"] != tx_id]
    if len(new) == len(txs):
        return False
    _update_user_list(user_id, "transactions", new)
    return True



def get_budgets(user_id: int) -> list:
    u = get_user(user_id)
    return u["budgets"] if u else []


def set_budget(user_id: int, category_id: int, amount: float, month: str) -> dict:
    budgets = get_budgets(user_id)
    for b in budgets:
        if b["category_id"] == category_id and b["month"] == month:
            b["amount"] = amount
            _update_user_list(user_id, "budgets", budgets)
            return b
    record = {
        "id":          _next_id(budgets),
        "created_at":  _now(),
        "category_id": category_id,
        "amount":      amount,
        "month":       month,
    }
    budgets.append(record)
    _update_user_list(user_id, "budgets", budgets)
    return record


def delete_budget(user_id: int, budget_id: int) -> bool:
    budgets = get_budgets(user_id)
    new = [b for b in budgets if b["id"] != budget_id]
    if len(new) == len(budgets):
        return False
    _update_user_list(user_id, "budgets", new)
    return True



def get_goals(user_id: int) -> list:
    u = get_user(user_id)
    return u["goals"] if u else []


def add_goal(user_id: int, data: dict) -> dict:
    goals = get_goals(user_id)
    record = {"id": _next_id(goals), "created_at": _now(), **data}
    goals.append(record)
    _update_user_list(user_id, "goals", goals)
    return record


def update_goal(user_id: int, goal_id: int, **kwargs) -> bool:
    goals = get_goals(user_id)
    for g in goals:
        if g["id"] == goal_id:
            g.update(kwargs)
            _update_user_list(user_id, "goals", goals)
            return True
    return False


def delete_goal(user_id: int, goal_id: int) -> bool:
    goals = get_goals(user_id)
    new = [g for g in goals if g["id"] != goal_id]
    if len(new) == len(goals):
        return False
    _update_user_list(user_id, "goals", new)
    return True



def init_data():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        _write({"users": []})
