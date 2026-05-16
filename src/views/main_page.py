import flet as ft
from src.models import *

def home_view(page):


    def open_menu_dialog(page):
        async def go(e, route):
            page.close(dlg)
            await page.push_route(route)

        items = [
            (ft.Icons.HOME_OUTLINED, "Головна"),
            (ft.Icons.DASHBOARD_OUTLINED, "Панель керування"),
            (ft.Icons.SWAP_HORIZ, "Транзакції"),
            (ft.Icons.PIE_CHART_OUTLINE, "Бюджет"),
            (ft.Icons.FLAG_OUTLINED, "Цілі"),
            (ft.Icons.BAR_CHART_OUTLINED, "Звіти"),
            (ft.Icons.CATEGORY_OUTLINED, "Категорії"),
            (ft.Icons.SETTINGS_OUTLINED, "Налаштування"),
        ]

        nav_items = [ft.Button(
                    icon=ft.Icon(icon, color=ft.Colors.WHITE),
                    content = label,
                    bgcolor = ft.Colors.ORANGE_900,
                    width = float("inf"),
                    height = 70,
                    color=ft.Colors.WHITE,
                    style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius=10), overlay_color = ft.Colors.ORANGE_700, ),
                )
                for icon, label in items
        ]


        dlg = ft.AlertDialog(
            bgcolor=ft.Colors.RED_900,
            alignment=ft.Alignment.TOP_LEFT,
            content=ft.Column(
                tight=True,
                width=300,
                controls=[
                    ft.Container(
                        bgcolor=ft.Colors.ORANGE_900,
                        padding=ft.Padding.symmetric(vertical=20, horizontal=20),
                        border_radius=ft.border_radius.only(top_left=12, top_right=12),
                        content=ft.Row(
                            controls=[
                                ft.CircleAvatar(
                                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=28),
                                    bgcolor=ft.Colors.RED_900,
                                    radius=28,
                                ),
                                ft.Text("Finance helper", color=ft.Colors.WHITE,
                                        size=16, weight=ft.FontWeight.BOLD),
                            ],
                            spacing=12,
                        ),

                    ),
                    ft.Divider(color=ft.Colors.ORANGE_700, height=1),
                    *nav_items,
                ],
            ),
        )

        page.show_dialog(dlg)


    def you_are_on_home_page_func(e):
        message_you_are_on_home_page = ft.SnackBar(ft.Text("Ви зараз на головній сторінці", color = ft.Colors.WHITE), bgcolor = ft.Colors.RED_900)
        page.show_dialog(message_you_are_on_home_page)


    async def open_register(e):
        await page.push_route("/login")

    main_bg_gradient = ft.Container(
        gradient = ft.RadialGradient(
                            center=ft.Alignment.CENTER,
                            radius=1.3,
                            colors=[ft.Colors.YELLOW_700, ft.Colors.ORANGE_900,],
                            stops=[0.0, 1.0],
        ),
        expand=True,
        height = 1000,
        alignment = ft.Alignment.CENTER
    )

    bottom_bar = ft.BottomAppBar(
        bgcolor=ft.Colors.ORANGE_900,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(ft.Icons.MENU, on_click=lambda e: open_menu_dialog(page), ),
                ft.IconButton(ft.Icons.HOME, on_click=you_are_on_home_page_func),
                ft.IconButton(ft.Icons.SETTINGS),
            ],
        ),
    )

    app_bar = ft.Container(
        content=ft.AppBar(
            title=ft.Text("Finance helper"),
            actions=[
                ft.IconButton(
                    ft.Icons.SETTINGS,
                    on_click=open_register,
                )
            ],
            bgcolor=ft.Colors.ORANGE_900,
            automatically_imply_leading=False
        ),
        bgcolor=ft.Colors.ORANGE_900,
        padding=15,
    )

    return ft.View(
        route="/",
        padding = 0,
        bottom_appbar = bottom_bar,
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor =ft.Colors.ORANGE_900 ,
        controls=[ft.Column([
                app_bar,
                main_bg_gradient,
            ]
            )
        ]
    )