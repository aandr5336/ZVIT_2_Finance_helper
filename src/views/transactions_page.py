import flet as ft
from src.models import *
from src.assets import *


def transactions_view(page):


    async def go_home(e):
        page.pop_dialog()
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
        await page.push_route("/categories")


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

    search_field = ft.TextField(
        hint_text="Пошук транзакцій...",
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

    header_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Транзакції",
                                    color=ft.Colors.WHITE,
                                    size=22,
                                    weight=ft.FontWeight.W_700,
                                ),
                                ft.Text(
                                    "Травень 2025 • 38 операцій",
                                    color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                                    size=13,
                                ),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                        ft.Button(
                            "+ Додати",
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
                ft.Container(height=4),
                search_field,
                ft.Container(height=4),
                ft.Row(
                    controls=[
                        ft.Button(
                            label,
                            bgcolor=ft.Colors.ORANGE_700 if label == "Всі" else ft.Colors.with_opacity(0.07,
                                                                                                       ft.Colors.WHITE),
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                elevation=0,
                            ),
                            height=34,
                        )
                        for label in ["Всі", "Дохід", "Витрати", "Переказ"]
                    ],
                    spacing=8,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ],
            spacing=8,
        ),
        padding=ft.Padding(left=20, right=20, top=20, bottom=12),
    )


    def summary_card(label, amount, color, icon):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, color=color, size=18),
                    ft.Text(amount, color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.W_700),
                    ft.Text(label, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=11),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=12, right=12, top=14, bottom=14),
            expand=True,
        )

    summary_row = ft.Container(
        content=ft.Row(
            controls=[
                summary_card("Дохід", "₴24 000", ft.Colors.GREEN_400, ft.Icons.ARROW_UPWARD),
                summary_card("Витрати", "₴12 480", ft.Colors.RED_400, ft.Icons.ARROW_DOWNWARD),
                summary_card("Різниця", "₴11 520", ft.Colors.ORANGE_300, ft.Icons.BALANCE_OUTLINED),
            ],
            spacing=10,
        ),
        padding=ft.Padding(left=20, right=20, top=0, bottom=12),
    )


    def transaction_item(icon, title, category, date, amount, is_expense):
        color = ft.Colors.RED_400 if is_expense else ft.Colors.GREEN_400
        sign = "-" if is_expense else "+"
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=ft.Colors.ORANGE_400, size=18),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_400),
                        border_radius=10,
                        padding=10,
                        width=42,
                        height=42,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_500),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(
                                            category,
                                            color=ft.Colors.ORANGE_300,
                                            size=11,
                                        ),
                                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_300),
                                        border_radius=4,
                                        padding=ft.Padding(left=6, right=6, top=2, bottom=2),
                                    ),
                                    ft.Text(
                                        date,
                                        color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE),
                                        size=11,
                                    ),
                                ],
                                spacing=6,
                            ),
                        ],
                        spacing=4,
                        expand=True,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"{sign}₴{amount}",
                                color=color,
                                size=15,
                                weight=ft.FontWeight.W_600,
                            ),
                            ft.Icon(
                                ft.Icons.CHEVRON_RIGHT,
                                color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                                size=16,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        spacing=2,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.07, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=14, right=14, top=12, bottom=12),
            ink=True,
            on_click=lambda e: None,
        )

    def day_group(date_label, items):
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        date_label,
                        color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                        size=12,
                        weight=ft.FontWeight.W_600,
                    ),
                    padding=ft.Padding(left=4, right=0, top=0, bottom=0),
                ),
                *items,
            ],
            spacing=6,
        )

    transactions_list = ft.Container(
        content=ft.Column(
            controls=[
                day_group("Сьогодні, -- місяця", [
                    transaction_item(ft.Icons.SHOPPING_CART_OUTLINED, "Сільпо", "Їжа", "14:32", "320", True),
                    transaction_item(ft.Icons.LOCAL_CAFE_OUTLINED, "Starbucks", "Кафе", "10:15", "85", True),
                ]),
                day_group("Вчора, -- місяця", [
                    transaction_item(ft.Icons.WORK_OUTLINE, "Зарплата", "Дохід", "09:00", "24 000", False),
                    transaction_item(ft.Icons.DIRECTIONS_BUS_OUTLINED, "Київ Пасажир", "Транспорт", "08:20", "45", True),
                    transaction_item(ft.Icons.WIFI_OUTLINED, "Київстар", "Комунальні", "08:00", "180", True),
                ]),
                day_group("-- місяця", [
                    transaction_item(ft.Icons.SPORTS_OUTLINED, "Спортзал FitCurves", "Здоров'я", "18:00", "600", True),
                    transaction_item(ft.Icons.MOVIE_OUTLINED, "Multiplex", "Розваги", "15:30", "240", True),
                    transaction_item(ft.Icons.CARD_GIFTCARD_OUTLINED, "Подарунок від мами", "Інше", "12:00", "500", False),
                ]),
                day_group("-- місяця", [
                    transaction_item(ft.Icons.LOCAL_PHARMACY_OUTLINED, "Аптека", "Здоров'я", "17:45", "156", True),
                    transaction_item(ft.Icons.RESTAURANT_OUTLINED, "Ресторан Київ", "Їжа", "13:00", "480", True),
                ]),
            ],
            spacing=20,
        ),
        padding=ft.Padding(left=20, right=20, top=4, bottom=24),
    )

    return ft.View(
        route="/transactions",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            header_section,
                            summary_row,
                            transactions_list,
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