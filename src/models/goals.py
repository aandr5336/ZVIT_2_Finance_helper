from src.storage import (
    get_goals as store_get, add_goal as store_add,
    update_goal as store_update, delete_goal as store_delete, Session,
)


def add_goal(title: str, target: float, description: str = "",
             deadline: str = "", icon: str = "flag", color: str = "#FF9800") -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    if not title.strip():
        return False, "Введіть назву цілі"
    if target <= 0:
        return False, "Сума має бути більше нуля"

    store_add(Session.user_id(), {
        "title":       title.strip(),
        "description": description.strip(),
        "target":      target,
        "saved":       0.0,
        "deadline":    deadline or None,
        "icon":        icon,
        "color":       color,
        "is_done":     False,
    })
    return True, "Ціль створено"


def delete_goal(goal_id: int) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    store_delete(Session.user_id(), goal_id)
    return True, "Ціль видалено"


def add_savings(goal_id: int, amount: float) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    if amount <= 0:
        return False, "Сума має бути більше нуля"

    goals = store_get(Session.user_id())
    goal = next((g for g in goals if g["id"] == goal_id), None)
    if not goal:
        return False, "Ціль не знайдена"

    new_saved = goal["saved"] + amount
    is_done = new_saved >= goal["target"]
    store_update(Session.user_id(), goal_id, saved=new_saved, is_done=is_done)

    if is_done:
        return True, "Ціль досягнута! 🎉"
    return True, f"Поповнено на ₴{amount:,.0f}"


def update_goal(goal_id: int, title: str, target: float,
                description: str = "", deadline: str = "") -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    if not title.strip():
        return False, "Введіть назву"
    if target <= 0:
        return False, "Сума має бути більше нуля"

    store_update(Session.user_id(), goal_id,
                 title=title.strip(), target=target,
                 description=description.strip(), deadline=deadline or None)
    return True, "Ціль оновлено"


def get_goals(only_active: bool = False) -> list:
    if not Session.is_logged_in():
        return []

    rows = store_get(Session.user_id())
    if only_active:
        rows = [r for r in rows if not r["is_done"]]

    rows = sorted(rows, key=lambda r: (r["is_done"], r["created_at"]))

    result = []
    for r in rows:
        d = dict(r)
        d["percent"] = min(d["saved"] / d["target"], 1.0) if d["target"] > 0 else 0
        d["remaining"] = max(d["target"] - d["saved"], 0)
        result.append(d)
    return result


def get_goals_summary() -> dict:
    goals = get_goals()
    return {
        "total":        len(goals),
        "active":       sum(1 for g in goals if not g["is_done"]),
        "done":         sum(1 for g in goals if g["is_done"]),
        "total_saved":  sum(g["saved"] for g in goals),
        "total_target": sum(g["target"] for g in goals),
    }
