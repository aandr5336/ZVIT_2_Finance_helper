import flet as ft

from src.views.control_panel_page import control_panel_view
from views import *


def main(page: ft.Page):
    page.title = "Finance helper"
    page.fonts = {
        "AmaticSC": "AmaticSC-Bold.ttf",
        "FiraCode":"FiraCode-SemiBold.ttf",
        "Lobster":"Lobster-Regular.ttf",
        "Manrope":"Manrope-Medium.ttf",
        "Poppins":"Poppins-Medium.ttf",
        "Nunito-Sans":"NunitoSans-Italic-VariableFont_YTLC,opsz,wdth,wght.ttf"
    }

    def route_change():
        page.views.clear()
        page.views.append(home_view(page))
        if page.route == "/":
            page.views.append(home_view(page))
        elif page.route == "/register":
            page.views.append(register_view(page))
        elif page.route == "/login":
            page.views.append(login_view(page))
        elif page.route == "/control_panel":
            page.views.append(control_panel_view(page))
        elif page.route == "/transactions":
            page.views.append(transactions_view(page))
        elif page.route == "/budget":
            page.views.append(budget_view(page))
        elif page.route == "/goals":
            page.views.append(goals_view(page))
        page.update()


    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            await page.push_route(page.views[-1].route)


    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.route = "/goals"
    route_change()


if __name__ == '__main__':
    ft.run(main, view=ft.AppView.WEB_BROWSER)