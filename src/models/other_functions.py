import flet as ft
from datetime import datetime


def home_page_message(page: ft.Page, is_home: bool):
    if is_home:
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text("Ви вже на головній сторінці", color=ft.Colors.WHITE),
                bgcolor=ft.Colors.ORANGE_900,
                duration=2000,
            )
        )


def current_month() -> str:
    return datetime.now().strftime("%Y-%m")


def format_currency(amount: float) -> str:
    from src.storage.session import Currency
    return Currency.format(amount)


def format_month_label(month: str) -> str:
    months_ua = {
        "01": "Січень", "02": "Лютий", "03": "Березень",
        "04": "Квітень", "05": "Травень", "06": "Червень",
        "07": "Липень", "08": "Серпень", "09": "Вересень",
        "10": "Жовтень", "11": "Листопад", "12": "Грудень",
    }
    try:
        year, m = month.split("-")
        return f"{months_ua.get(m, m)} {year}"
    except Exception:
        return month


def prev_month(month: str) -> str:
    year, m = int(month[:4]), int(month[5:])
    m -= 1
    if m == 0:
        m, year = 12, year - 1
    return f"{year}-{m:02d}"


def next_month(month: str) -> str:
    year, m = int(month[:4]), int(month[5:])
    m += 1
    if m == 13:
        m, year = 1, year + 1
    return f"{year}-{m:02d}"


