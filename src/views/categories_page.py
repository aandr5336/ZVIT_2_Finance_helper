import flet as ft
from src.models import *
from src.assets import *


def categories_view(page):


    async def go_home(e):
        await page.push_route("/")


    async def go_control_panel(e):
        await page.push_route("/control_panel")


    async def go_transactions(e):
        await page.push_route("/transactions")


    async def go_budget(e):
        await page.push_route("/budget")


    async def go_goals(e):
        await page.push_route("/goals")


    async def go_reports(e):
        await page.push_route("/reports")


    async def go_categories(e):
        page.pop_dialog()
        page.show_dialog(
            ft.SnackBar(
                ft.Text("Ви зараз на сторінці категорій.", color = ft.Colors.WHITE),
                bgcolor = ft.Colors.ORANGE_600,
            )
        )


    async def go_settings(e):
        await page.push_route("/settings")




    custom_appbar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SHOW_CHART, color=ft.Colors.ORANGE_300, size=20),
                        ft.Text(
                            "Finance Helper",
                            color=ft.Colors.WHITE,
                            size=18,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=8,
                    expand=True,
                ),
                ft.IconButton(
                    ft.Icons.SETTINGS_OUTLINED,
                    icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                    icon_size=20,
                    on_click=lambda e: open_settings_dialog(page),
                ),
                ft.IconButton(
                    ft.Icons.MENU,
                    icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                    icon_size=20,
                    on_click=lambda e: open_left_menu_dialog(page, go_home, go_control_panel, go_transactions, go_budget, go_goals, go_reports, go_categories, go_settings),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        gradient=gradient_for_appbar,
        height=60,
        padding=ft.Padding(left=20, right=8, top=0, bottom=0),
        border=ft.Border(
            bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE))
        ),
    )


    header_section = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "Категорії",
                            color=ft.Colors.WHITE,
                            size=22,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "12 категорій • 3 групи",
                            color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                            size=13,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.Button(
                    "+ Категорія",
                    bgcolor=ft.Colors.ORANGE_700,
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        elevation=0,
                    ),
                    height=38,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(left=20, right=20, top=20, bottom=12),
    )


    search_field = ft.TextField(
        hint_text="Пошук категорій...",
        border_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        focused_border_color=ft.Colors.ORANGE_400,
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border_radius=10,
        height=44,
        text_style=ft.TextStyle(color=ft.Colors.WHITE, size=14),
        hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE)),
        prefix_icon=ft.Icons.SEARCH,
        content_padding=ft.Padding(left=0, right=12, top=0, bottom=0),
    )

    search_container = ft.Container(
        content=search_field,
        padding=ft.Padding(left=20, right=20, top=0, bottom=12),
    )


    type_switcher = ft.Container(
        content=ft.Row(
            controls=[
                ft.Button(
                    label,
                    bgcolor=ft.Colors.ORANGE_700 if label == "Витрати" else ft.Colors.with_opacity(0.0, ft.Colors.WHITE),
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=0,
                    ),
                    height=34,
                )
                for label in ["Витрати", "Дохід", "Всі"]
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=12,
        padding=6,
        margin=ft.Margin.symmetric(horizontal=20, vertical=4),
    )


    def category_card(icon, label, amount, tx_count, color, is_income=False):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=20),
                                bgcolor=ft.Colors.with_opacity(0.12, color),
                                border_radius=10,
                                padding=10,
                                width=42,
                                height=42,
                            ),
                            ft.Container(expand=True),
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        ft.Icons.EDIT_OUTLINED,
                                        icon_color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE),
                                        icon_size=16,
                                        on_click=lambda e: None,
                                    ),
                                    ft.IconButton(
                                        ft.Icons.DELETE_OUTLINE,
                                        icon_color=ft.Colors.with_opacity(0.25, ft.Colors.RED_300),
                                        icon_size=16,
                                        on_click=lambda e: None,
                                    ),
                                ],
                                spacing=0,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        label,
                        color=ft.Colors.WHITE,
                        size=14,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Text(
                        f"₴{amount:,}",
                        color=color,
                        size=16,
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(
                        f"{tx_count} транзакцій",
                        color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE),
                        size=11,
                    ),
                ],
                spacing=2,
            ),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.09, ft.Colors.WHITE)),
            border_radius=14,
            padding=14,
            ink=True,
            on_click=lambda e: None,
        )


    def category_group(title, icon, cards):
        grid = ft.ResponsiveRow(
            controls=[
                ft.Column(
                    controls=[card],
                    col={"xs": 6},
                )
                for card in cards
            ],
            spacing=10,
            run_spacing=10,
        )
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(icon, color=ft.Colors.ORANGE_400, size=16),
                            ft.Text(
                                title,
                                color=ft.Colors.WHITE,
                                size=15,
                                weight=ft.FontWeight.W_700,
                            ),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=4),
                    grid,
                ],
                spacing=8,
            ),
        )

    expense_group = category_group(
        "Всі категорії",
        ft.Icons.SHOPPING_CART_OUTLINED,
        [
            category_card(ft.Icons.RESTAURANT_OUTLINED, "Їжа та напої", 3200, 14, ft.Colors.ORANGE_400),
            category_card(ft.Icons.DIRECTIONS_BUS_OUTLINED, "Транспорт", 850, 8, ft.Colors.BLUE_400),
            category_card(ft.Icons.LOCAL_CAFE_OUTLINED, "Кафе", 640, 6, ft.Colors.BROWN_300),
            category_card(ft.Icons.SHOPPING_BAG_OUTLINED, "Покупки", 2100, 11, ft.Colors.PINK_300),
            category_card(ft.Icons.SPORTS_OUTLINED, "Здоров'я", 1356, 5, ft.Colors.GREEN_400),
            category_card(ft.Icons.MOVIE_OUTLINED, "Розваги", 1200, 7, ft.Colors.PURPLE_300),
            category_card(ft.Icons.BOOK_OUTLINED, "Освіта", 480, 2, ft.Colors.CYAN_400),
            category_card(ft.Icons.FLIGHT_OUTLINED, "Подорожі", 0, 0, ft.Colors.TEAL_400),
            category_card(ft.Icons.BOLT_OUTLINED, "Комунальні", 860, 4, ft.Colors.YELLOW_600),
            category_card(ft.Icons.WIFI_OUTLINED, "Інтернет", 180, 1, ft.Colors.BLUE_300),
            category_card(ft.Icons.LOCAL_HOSPITAL_OUTLINED, "Медицина", 320, 2, ft.Colors.RED_300),
            category_card(ft.Icons.MORE_HORIZ, "Інше", 294, 3, ft.Colors.GREY_400),
        ],
    )


    stats_row = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("12", color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.W_700),
                        ft.Text("Категорій", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=3,
                    expand=True,
                ),
                ft.Container(width=1, height=36, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                ft.Column(
                    controls=[
                        ft.Text("58", color=ft.Colors.ORANGE_300, size=20, weight=ft.FontWeight.W_700),
                        ft.Text("Транзакцій", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=3,
                    expand=True,
                ),
                ft.Container(width=1, height=36, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                ft.Column(
                    controls=[
                        ft.Text("₴11 480", color=ft.Colors.RED_400, size=20, weight=ft.FontWeight.W_700),
                        ft.Text("Всього витрат", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=3,
                    expand=True,
                ),
            ],
        ),
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=14,
        padding=ft.Padding(left=16, right=16, top=16, bottom=16),
        margin=ft.Margin.symmetric(horizontal=20, vertical=4),
    )

    categories_content = ft.Container(
        content=ft.Column(
            controls=[
                expense_group,
            ],
            spacing=20,
        ),
        padding=ft.Padding(left=20, right=20, top=8, bottom=24),
    )

    return ft.View(
        route="/categories",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            header_section,
                            search_container,
                            type_switcher,
                            stats_row,
                            categories_content,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        spacing=0,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ],
    )