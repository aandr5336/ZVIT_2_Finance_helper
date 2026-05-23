import flet as ft
from views import *


def main(page: ft.Page):


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
        elif page.route == "/reports":
            page.views.append(reports_view(page))
        elif page.route == "/categories":
            page.views.append(categories_view(page))
        elif page.route == "/settings":
            page.views.append(settings_view(page))

        page.update()

    async def view_pop(e):

        if len(page.views) > 1:
            page.views.pop()

            await page.push_route(page.views[-1].route)

    page.on_route_change = route_change

    page.on_view_pop = view_pop

    route_change()

if __name__ == '__main__':
    ft.run(main, view=ft.AppView.WEB_BROWSER)