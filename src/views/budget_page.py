import flet as ft
from src.models import *
from src.assets import *


def budget_view(page):


    async def go_home(e):
        await page.push_route("/")


    async def go_control_panel(e):
        await page.push_route("/control_panel")


    async def go_transactions(e):
        await page.push_route("/transactions")


    async def go_budget(e):
        page.pop_dialog()
        page.show_dialog(
            ft.SnackBar(
                ft.Text("Ви зараз на сторінці бюджету.", color = ft.Colors.WHITE),
                bgcolor = ft.Colors.ORANGE_600,
            )
        )


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


    header_section = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "Бюджет",
                            color=ft.Colors.WHITE,
                            size=22,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "місяць 2025",
                            color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                            size=13,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.Button(
                    "+ Бюджет",
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


    overall_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Загальний бюджет",
                                    color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
                                    size=13,
                                ),
                                ft.Text(
                                    "₴ 9 500 / ₴ 15 000",
                                    color=ft.Colors.WHITE,
                                    size=24,
                                    weight=ft.FontWeight.W_700,
                                ),
                            ],
                            spacing=4,
                            expand=True,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "63%",
                                color=ft.Colors.ORANGE_300,
                                size=22,
                                weight=ft.FontWeight.W_700,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_300),
                            border_radius=12,
                            padding=ft.Padding(left=14, right=14, top=10, bottom=10),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=12),
                ft.Stack(
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                            border_radius=6,
                            height=10,
                        ),
                        ft.Container(
                            gradient=ft.LinearGradient(
                                begin=ft.Alignment(-1, 0),
                                end=ft.Alignment(1, 0),
                                colors=[ft.Colors.ORANGE_700, ft.Colors.ORANGE_400],
                            ),
                            border_radius=6,
                            height=10,
                            width=400 * 0.63,
                        ),
                    ],
                ),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    width=8, height=8,
                                    bgcolor=ft.Colors.GREEN_400,
                                    border_radius=4,
                                ),
                                ft.Text(
                                    "Залишилось ₴5 500",
                                    color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE),
                                    size=12,
                                ),
                            ],
                            spacing=6,
                        ),
                        ft.Text(
                            "10 днів до кінця місяця",
                            color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE),
                            size=12,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=0,
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[
                ft.Colors.with_opacity(0.18, ft.Colors.ORANGE_700),
                ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
            ],
        ),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.ORANGE_400)),
        border_radius=16,
        padding=20,
        margin=ft.Margin.symmetric(horizontal=20, vertical=4),
    )


    month_switcher = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    ft.Icons.CHEVRON_LEFT,
                    icon_color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
                    icon_size=20,
                ),
                ft.Text(
                    "місяць 2025",
                    color=ft.Colors.WHITE,
                    size=14,
                    weight=ft.FontWeight.W_600,
                    expand=True,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.IconButton(
                    ft.Icons.CHEVRON_RIGHT,
                    icon_color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
                    icon_size=20,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=10,
        margin=ft.Margin.symmetric(horizontal=20, vertical=8),
        padding=ft.Padding(left=4, right=4, top=4, bottom=4),
    )


    def budget_card(icon, label, spent, total, color):
        percent = min(spent / total, 1.0)
        is_over = spent > total
        status_color = ft.Colors.RED_400 if is_over else ft.Colors.GREEN_400
        status_text = "Перевищено!" if is_over else f"Залишилось ₴{total - spent:,}"

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
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        label,
                                        color=ft.Colors.WHITE,
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    ft.Text(
                                        status_text,
                                        color=status_color,
                                        size=11,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        f"₴{spent:,}",
                                        color=ft.Colors.WHITE,
                                        size=15,
                                        weight=ft.FontWeight.W_700,
                                    ),
                                    ft.Text(
                                        f"з ₴{total:,}",
                                        color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                        size=11,
                                    ),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Stack(
                        controls=[
                            ft.Container(
                                bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                                border_radius=4,
                                height=6,
                            ),
                            ft.Container(
                                bgcolor=color if not is_over else ft.Colors.RED_400,
                                border_radius=4,
                                height=6,
                                width=260 * percent,
                            ),
                        ],
                    ),
                    ft.Container(height=2),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"{int(percent * 100)}% використано",
                                color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                size=11,
                            ),
                            ft.TextButton(
                                "Редагувати",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.ORANGE_400,
                                    padding=ft.Padding(left=0, right=0, top=0, bottom=0),
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
            border_radius=14,
            padding=16,
        )

    budgets_data = [
        (ft.Icons.RESTAURANT_OUTLINED, "Їжа та напої", 3200, 5000, ft.Colors.ORANGE_400),
        (ft.Icons.DIRECTIONS_BUS_OUTLINED, "Транспорт", 850, 1500, ft.Colors.BLUE_400),
        (ft.Icons.MOVIE_OUTLINED, "Розваги", 1200, 1000, ft.Colors.PURPLE_300),
        (ft.Icons.BOLT_OUTLINED, "Комунальні", 680, 2000, ft.Colors.GREEN_400),
        (ft.Icons.LOCAL_HOSPITAL_OUTLINED, "Здоров'я", 756, 1500, ft.Colors.RED_300),
        (ft.Icons.SHOPPING_BAG_OUTLINED, "Покупки", 2100, 2000, ft.Colors.PINK_300),
    ]

    budgets_list = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Категорії бюджету",
                        color=ft.Colors.WHITE,
                        size=16,
                        weight=ft.FontWeight.W_700,
                    ),
                    padding=ft.Padding(left=0, right=0, top=0, bottom=4),
                ),
                *[budget_card(icon, label, spent, total, color)
                  for icon, label, spent, total, color in budgets_data],
            ],
            spacing=10,
        ),
        padding=ft.Padding(left=20, right=20, top=8, bottom=24),
    )

    return ft.View(
        route="/budget",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            header_section,
                            overall_card,
                            month_switcher,
                            budgets_list,
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