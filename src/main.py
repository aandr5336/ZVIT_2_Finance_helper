import flet as ft
from views import *


def main(page: ft.Page):
    page.title = "Finance helper"

    def route_change():
        page.views.clear()
        page.views.append(login_view(page))
        if page.route == "/":
            page.views.append(home_view(page))
        if page.route == "/register":
            page.views.append(register_view(page))
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