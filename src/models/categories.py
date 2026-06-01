from src.storage import (
    get_categories as store_get, add_category as store_add,
    update_category as store_update, delete_category as store_delete,
    get_transactions, Session,
)


def add_category(name: str, icon: str, color: str, cat_type: str) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    if not name.strip():
        return False, "Введіть назву"
    if cat_type not in ("expense", "income"):
        return False, "Невірний тип"
    store_add(Session.user_id(), {"name": name.strip(), "icon": icon, "color": color, "type": cat_type})
    return True, "Категорію додано"


def update_category(category_id: int, name: str, icon: str, color: str) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    if not name.strip():
        return False, "Введіть назву"
    store_update(Session.user_id(), category_id, name=name.strip(), icon=icon, color=color)
    return True, "Категорію оновлено"


def delete_category(category_id: int) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    store_delete(Session.user_id(), category_id)
    return True, "Категорію видалено"


def get_categories(cat_type=None) -> list:
    if not Session.is_logged_in():
        return []

    uid = Session.user_id()
    cats = store_get(uid)
    if cat_type:
        cats = [c for c in cats if c["type"] == cat_type]

    all_tx = get_transactions(uid)
    result = []
    for c in cats:
        tx = [t for t in all_tx if t.get("category_id") == c["id"]]
        result.append({**c, "tx_count": len(tx), "total": sum(t["amount"] for t in tx)})
    return sorted(result, key=lambda x: x["total"], reverse=True)
