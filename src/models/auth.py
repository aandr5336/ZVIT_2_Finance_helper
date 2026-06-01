import hashlib
from src.storage import get_user_by_email, create_user, update_user, add_category, Session


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(name: str, email: str, password: str, confirm: str) -> tuple:
    name = name.strip()
    email = email.strip().lower()

    if not name:
        return False, "Введіть ім'я"
    if not email or "@" not in email:
        return False, "Введіть коректний email"
    if len(password) < 6:
        return False, "Пароль має бути не менше 6 символів"
    if password != confirm:
        return False, "Паролі не співпадають"
    if get_user_by_email(email):
        return False, "Користувач з таким email вже існує"

    user = create_user(name, email, _hash(password))
    _seed_default_categories(user["id"])
    return True, "Акаунт створено успішно"


def login_user(email: str, password: str) -> tuple:
    email = email.strip().lower()

    if not email or not password:
        return False, "Заповніть всі поля"

    user = get_user_by_email(email)
    if not user:
        return False, "Користувача з таким email не знайдено"
    if user["password"] != _hash(password):
        return False, "Невірний пароль"

    Session.login(user["id"], user["name"], user["email"])
    return True, "Вхід успішний"


def logout_user():
    Session.logout()


def change_password(old_password: str, new_password: str, confirm: str) -> tuple:
    if not Session.is_logged_in():
        return False, "Не авторизовано"
    if len(new_password) < 6:
        return False, "Новий пароль має бути не менше 6 символів"
    if new_password != confirm:
        return False, "Паролі не співпадають"

    user = get_user_by_email(Session.user_email())
    if not user or user["password"] != _hash(old_password):
        return False, "Старий пароль невірний"

    update_user(Session.user_id(), password=_hash(new_password))
    return True, "Пароль змінено успішно"


def _seed_default_categories(user_id: int):
    defaults = [
        ("Їжа та напої",  "restaurant",     "#FF9800", "expense"),
        ("Транспорт",     "directions_bus", "#2196F3", "expense"),
        ("Кафе",          "local_cafe",     "#795548", "expense"),
        ("Покупки",       "shopping_bag",   "#E91E63", "expense"),
        ("Здоров'я",      "sports",         "#4CAF50", "expense"),
        ("Розваги",       "movie",          "#9C27B0", "expense"),
        ("Освіта",        "book",           "#00BCD4", "expense"),
        ("Подорожі",      "flight",         "#009688", "expense"),
        ("Комунальні",    "bolt",           "#FFC107", "expense"),
        ("Інтернет",      "wifi",           "#03A9F4", "expense"),
        ("Медицина",      "local_hospital", "#F44336", "expense"),
        ("Зарплата",      "work",           "#4CAF50", "income"),
        ("Фріланс",       "laptop",         "#8BC34A", "income"),
        ("Подарунки",     "card_giftcard",  "#FF5722", "income"),
    ]
    for name, icon, color, cat_type in defaults:
        add_category(user_id, {"name": name, "icon": icon, "color": color, "type": cat_type})
