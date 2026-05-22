import flet as ft
from src.models import *
from src.assets import *


def control_panel_view(page):

    async def go_home():
        await page.push_route("/")


    async def go_control_panel():
        await page.push_route("/control_panel")


    async def go_transactions():
        await page.push_route("/transactions")


    async def go_budget():
        await page.push_route("/budget")


    async def go_goals():
        await page.push_route("/goals")


    async def go_reports():
        await page.push_route("/reports")


    async def go_categories():
        await page.push_route("/categories")


    async def go_settings():
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


    greeting = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "Привіт, ",
                            color=ft.Colors.WHITE,
                            size=22,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "Ось твій фінансовий огляд за травень",
                            color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                            size=13,
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.Button(
                    "+ Транзакція",
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
        padding=ft.Padding(left=20, right=20, top=20, bottom=8),
    )


    balance_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Загальний баланс",
                            color=ft.Colors.with_opacity(0.65, ft.Colors.WHITE),
                            size=13,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Травень 2025",
                                color=ft.Colors.ORANGE_300,
                                size=12,
                                weight=ft.FontWeight.W_500,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_300),
                            border_radius=6,
                            padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(
                    "₴ 48 320,00",
                    color=ft.Colors.WHITE,
                    size=36,
                    weight=ft.FontWeight.W_700,
                ),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.GREEN_400, size=14),
                                        ft.Text("Дохід", color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE), size=12),
                                    ],
                                    spacing=4,
                                ),
                                ft.Text("₴ 24 000", color=ft.Colors.GREEN_400, size=16, weight=ft.FontWeight.W_600),
                            ],
                            spacing=2,
                        ),
                        ft.Container(
                            width=1, height=36,
                            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.RED_400, size=14),
                                        ft.Text("Витрати", color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE), size=12),
                                    ],
                                    spacing=4,
                                ),
                                ft.Text("₴ 12 480", color=ft.Colors.RED_400, size=16, weight=ft.FontWeight.W_600),
                            ],
                            spacing=2,
                        ),
                        ft.Container(
                            width=1, height=36,
                            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                        ),
                        ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.SAVINGS_OUTLINED, color=ft.Colors.ORANGE_300, size=14),
                                        ft.Text("Заощаджено", color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE), size=12),
                                    ],
                                    spacing=4,
                                ),
                                ft.Text("₴ 11 520", color=ft.Colors.ORANGE_300, size=16, weight=ft.FontWeight.W_600),
                            ],
                            spacing=2,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
            ],
            spacing=8,
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[ft.Colors.with_opacity(0.18, ft.Colors.ORANGE_700), ft.Colors.with_opacity(0.08, ft.Colors.WHITE)],
        ),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.ORANGE_400)),
        border_radius=16,
        padding=20,
        margin=ft.Margin.symmetric(horizontal=20, vertical=8),
    )


    def stat_card(icon, label, value, color, trend=None):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=18),
                                bgcolor=ft.Colors.with_opacity(0.12, color),
                                border_radius=8,
                                padding=8,
                                width=36,
                                height=36,
                            ),
                            ft.Text(
                                trend or "",
                                color=ft.Colors.GREEN_400 if trend and "+" in trend else ft.Colors.RED_400,
                                size=12,
                                weight=ft.FontWeight.W_500,
                            ) if trend else ft.Container(),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=8),
                    ft.Text(value, color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.W_700),
                    ft.Text(label, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=12),
                ],
                spacing=2,
            ),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
            border_radius=14,
            padding=16,
            expand=True,
        )

    stat_cards = ft.Container(
        content=ft.Row(
            controls=[
                stat_card(ft.Icons.RECEIPT_OUTLINED, "Транзакцій", "38", ft.Colors.ORANGE_400, "+5"),
                stat_card(ft.Icons.PIE_CHART_OUTLINE, "Бюджетів", "4", ft.Colors.BLUE_300),
                stat_card(ft.Icons.FLAG_OUTLINED, "Цілей", "3", ft.Colors.GREEN_400, "+1"),
            ],
            spacing=12,
        ),
        padding=ft.Padding(left=20, right=20, top=4, bottom=4),
    )


    def transaction_item(icon, title, category, amount, is_expense):
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
                        width=40,
                        height=40,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_500),
                            ft.Text(category, color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=12),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Text(
                        f"{sign}₴{amount}",
                        color=color,
                        size=15,
                        weight=ft.FontWeight.W_600,
                    ),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.07, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=14, right=14, top=12, bottom=12),
        )

    transactions_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Останні транзакції",
                            color=ft.Colors.WHITE,
                            size=16,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.TextButton(
                            "Всі →",
                            style=ft.ButtonStyle(color=ft.Colors.ORANGE_400),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=4),
                transaction_item(ft.Icons.SHOPPING_CART_OUTLINED, "Продукти", "Їжа та напої", "320", True),
                transaction_item(ft.Icons.DIRECTIONS_BUS_OUTLINED, "Транспорт", "Проїзд", "45", True),
                transaction_item(ft.Icons.WORK_OUTLINE, "Зарплата", "Дохід", "24 000", False),
                transaction_item(ft.Icons.WIFI_OUTLINED, "Інтернет", "Комунальні", "180", True),
                transaction_item(ft.Icons.SPORTS_OUTLINED, "Спортзал", "Здоров'я", "600", True),
            ],
            spacing=8,
        ),
        padding=ft.Padding(left=20, right=20, top=8, bottom=8),
    )


    def budget_bar(label, spent, total, color):
        percent = spent / total
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(label, color=ft.Colors.with_opacity(0.75, ft.Colors.WHITE), size=13),
                        ft.Text(
                            f"₴{spent} / ₴{total}",
                            color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                            size=12,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.Container(
                        bgcolor=color,
                        border_radius=4,
                        width=None,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                    border_radius=4,
                    height=8,
                ),
            ],
            spacing=6,
        )

    budget_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            "Бюджет цього місяця",
                            color=ft.Colors.WHITE,
                            size=16,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.TextButton(
                            "Деталі →",
                            style=ft.ButtonStyle(color=ft.Colors.ORANGE_400),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=4),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            budget_bar("Їжа та напої", 3200, 5000, ft.Colors.ORANGE_400),
                            budget_bar("Транспорт", 850, 1500, ft.Colors.BLUE_400),
                            budget_bar("Розваги", 1200, 1000, ft.Colors.RED_400),
                            budget_bar("Комунальні", 680, 2000, ft.Colors.GREEN_400),
                        ],
                        spacing=14,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
                    border_radius=14,
                    padding=16,
                ),
            ],
            spacing=8,
        ),
        padding=ft.Padding(left=20, right=20, top=8, bottom=20),
    )

    return ft.View(
        route="/control_panel",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            greeting,
                            balance_card,
                            stat_cards,
                            transactions_section,
                            budget_section,
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