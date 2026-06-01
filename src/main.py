import flet as ft
from src.storage import init_data, Session
from src.views import *


def main(page: ft.Page):
    async def fetch_usd_rate() -> float:
        import urllib.request
        import json
        try:
            url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read())
            for item in data:
                if item.get("ccy") == "USD":
                    rate = float(item["sale"])
                    from src.storage.session import Currency
                    Currency.set_rate(rate)
                    return rate
        except Exception:
            pass
        return 41.0


    page.title = "Finance Helper"
    page.fonts = {
        "AmaticSC":    "AmaticSC-Bold.ttf",
        "FiraCode":    "FiraCode-SemiBold.ttf",
        "Lobster":     "Lobster-Regular.ttf",
        "Manrope":     "Manrope-Medium.ttf",
        "Poppins":     "Poppins-Medium.ttf",
        "Nunito-Sans": "NunitoSans-Italic-VariableFont_YTLC,opsz,wdth,wght.ttf",
    }

    init_data()
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.BLACK
    fetch_usd_rate()

    protected = [
        "/control_panel", "/transactions", "/budget",
        "/goals", "/reports", "/categories", "/settings",
    ]

    def route_change():
        page.views.clear()

        if page.route in protected and not Session.is_logged_in():
            page.views.append(login_view(page))
            page.update()
            return

        if page.route == "/":
            page.views.append(home_view(page))
        elif page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/register":
            page.views.append(register_view(page))
        elif page.route == "/control_panel":
            page.views.append(control_panel_view(page))
        elif page.route == "/transactions":
            page.views.append(transactions_view(page))
        elif page.route == "/budget":
            page.views.append(budget_view(page))
        elif page.route == "/goals":
            page.views.append(goals_view(page))
        elif page.route == "/reports":
            page.views.append(reports_view(page))
        elif page.route == "/categories":
            page.views.append(categories_view(page))
        elif page.route == "/settings":
            page.views.append(settings_view(page))
        else:
            page.views.append(home_view(page))

        page.update()

    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.route = "/"
    route_change()


if __name__ == "__main__":
    ft.run(main, view=ft.AppView.WEB_BROWSER)
