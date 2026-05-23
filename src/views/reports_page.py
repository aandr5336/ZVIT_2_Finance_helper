import flet as ft
from src.models import *
from src.assets import *


def reports_view(page):


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


    header_section = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            "Звіти",
                            color=ft.Colors.WHITE,
                            size=22,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "Аналітика та статистика",
                            color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                            size=13,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.Button(
                    "Експорт",
                    icon=ft.Icons.DOWNLOAD_OUTLINED,
                    bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
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


    period_switcher = ft.Container(
        content=ft.Row(
            controls=[
                ft.Button(
                    label,
                    bgcolor=ft.Colors.ORANGE_700 if label == "Місяць" else ft.Colors.with_opacity(0.0, ft.Colors.WHITE),
                    color=ft.Colors.WHITE,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        elevation=0,
                    ),
                    height=34,
                )
                for label in ["Тиждень", "Місяць", "Квартал", "Рік"]
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


    month_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Травень 2025",
                                    color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE),
                                    size=13,
                                ),
                                ft.Text(
                                    "Чистий дохід",
                                    color=ft.Colors.WHITE,
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                ),
                                ft.Text(
                                    "₴ 11 520",
                                    color=ft.Colors.GREEN_400,
                                    size=28,
                                    weight=ft.FontWeight.W_700,
                                ),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                        ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.GREEN_400, size=13),
                                            ft.Text("+8.3%", color=ft.Colors.GREEN_400, size=13, weight=ft.FontWeight.W_600),
                                        ],
                                        spacing=2,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400),
                                    border_radius=6,
                                    padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                                ),
                                ft.Text(
                                    "vs квітень",
                                    color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                    size=11,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=4,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=16),
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Дохід", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=12),
                                ft.Text("₴24 000", color=ft.Colors.GREEN_400, size=16, weight=ft.FontWeight.W_600),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                        ft.Container(width=1, height=32, bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
                        ft.Column(
                            controls=[
                                ft.Text("Витрати", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=12),
                                ft.Text("₴12 480", color=ft.Colors.RED_400, size=16, weight=ft.FontWeight.W_600),
                            ],
                            spacing=3,
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(width=1, height=32, bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
                        ft.Column(
                            controls=[
                                ft.Text("Заощадження", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=12),
                                ft.Text("48%", color=ft.Colors.ORANGE_300, size=16, weight=ft.FontWeight.W_600),
                            ],
                            spacing=3,
                            expand=True,
                            horizontal_alignment=ft.CrossAxisAlignment.END,
                        ),
                    ],
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
        margin=ft.Margin.symmetric(horizontal=20, vertical=8),
    )


    def bar_chart():
        months = [
            ("Січ", 8200, 15000),
            ("Лют", 9100, 16000),
            ("Бер", 7800, 14500),
            ("Квіт", 10600, 18000),
            ("Тра", 12480, 24000),
        ]
        max_val = max(income for _, _, income in months)

        bars = []
        for label, expense, income in months:
            income_h = int(120 * income / max_val)
            expense_h = int(120 * expense / max_val)
            bars.append(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREEN_400),
                                    border_radius=ft.BorderRadius.only(top_left=4, top_right=4),
                                    width=14,
                                    height=income_h,
                                ),
                                ft.Container(
                                    bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.RED_400),
                                    border_radius=ft.BorderRadius.only(top_left=4, top_right=4),
                                    width=14,
                                    height=expense_h,
                                ),
                            ],
                            spacing=3,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        ),
                        ft.Text(
                            label,
                            color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                            size=11,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                )
            )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Дохід vs Витрати",
                                color=ft.Colors.WHITE,
                                size=15,
                                weight=ft.FontWeight.W_700,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Row(controls=[
                                        ft.Container(width=10, height=10, bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREEN_400), border_radius=2),
                                        ft.Text("Дохід", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=11),
                                    ], spacing=4),
                                    ft.Row(controls=[
                                        ft.Container(width=10, height=10, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.RED_400), border_radius=2),
                                        ft.Text("Витрати", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=11),
                                    ], spacing=4),
                                ],
                                spacing=12,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        controls=bars,
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
            border_radius=14,
            padding=18,
        )


    def category_row(icon, label, amount, total_expenses, color):
        percent = amount / total_expenses
        bar_width = int(260 * percent)
        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icon, color=color, size=14),
                            bgcolor=ft.Colors.with_opacity(0.1, color),
                            border_radius=6,
                            padding=5,
                            width=26,
                            height=26,
                        ),
                        ft.Text(label, color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE), size=13, expand=True),
                        ft.Text(f"₴{amount:,}", color=ft.Colors.WHITE, size=13, weight=ft.FontWeight.W_600),
                        ft.Text(f"{int(percent * 100)}%", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=12),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Stack(
                    controls=[
                        ft.Container(bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE), border_radius=3, height=4),
                        ft.Container(bgcolor=color, border_radius=3, height=4, width=bar_width),
                    ],
                ),
            ],
            spacing=6,
        )

    categories_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Топ категорій витрат",
                    color=ft.Colors.WHITE,
                    size=15,
                    weight=ft.FontWeight.W_700,
                ),
                ft.Container(height=8),
                category_row(ft.Icons.RESTAURANT_OUTLINED, "Їжа та напої", 3200, 12480, ft.Colors.ORANGE_400),
                category_row(ft.Icons.SHOPPING_BAG_OUTLINED, "Покупки", 2100, 12480, ft.Colors.PINK_300),
                category_row(ft.Icons.SPORTS_OUTLINED, "Здоров'я", 1356, 12480, ft.Colors.GREEN_400),
                category_row(ft.Icons.MOVIE_OUTLINED, "Розваги", 1200, 12480, ft.Colors.PURPLE_300),
                category_row(ft.Icons.BOLT_OUTLINED, "Комунальні", 860, 12480, ft.Colors.BLUE_400),
                category_row(ft.Icons.DIRECTIONS_BUS_OUTLINED, "Транспорт", 850, 12480, ft.Colors.CYAN_400),
                category_row(ft.Icons.MORE_HORIZ, "Інше", 2914, 12480, ft.Colors.GREY_400),
            ],
            spacing=14,
        ),
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=14,
        padding=18,
    )


    def compare_row(label, current, previous):
        diff = current - previous
        is_up = diff > 0
        diff_color = ft.Colors.RED_400 if is_up else ft.Colors.GREEN_400
        arrow = ft.Icons.ARROW_UPWARD if is_up else ft.Icons.ARROW_DOWNWARD
        return ft.Row(
            controls=[
                ft.Text(label, color=ft.Colors.with_opacity(0.65, ft.Colors.WHITE), size=13, expand=True),
                ft.Text(f"₴{current:,}", color=ft.Colors.WHITE, size=13, weight=ft.FontWeight.W_500),
                ft.Row(
                    controls=[
                        ft.Icon(arrow, color=diff_color, size=13),
                        ft.Text(f"₴{abs(diff):,}", color=diff_color, size=12),
                    ],
                    spacing=2,
                ),
            ],
            spacing=10,
        )

    compare_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Порівняння з квітнем", color=ft.Colors.WHITE, size=15, weight=ft.FontWeight.W_700),
                    ],
                ),
                ft.Container(height=4),
                ft.Container(height=1, bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
                ft.Container(height=10),
                compare_row("Дохід", 24000, 22150),
                compare_row("Витрати", 12480, 13200),
                compare_row("Їжа", 3200, 2900),
                compare_row("Транспорт", 850, 920),
                compare_row("Розваги", 1200, 800),
            ],
            spacing=12,
        ),
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=14,
        padding=18,
    )

    charts_and_stats = ft.Container(
        content=ft.Column(
            controls=[
                bar_chart(),
                ft.Container(height=4),
                categories_section,
                ft.Container(height=4),
                compare_section,
            ],
            spacing=12,
        ),
        padding=ft.Padding(left=20, right=20, top=4, bottom=24),
    )

    return ft.View(
        route="/reports",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            header_section,
                            period_switcher,
                            month_card,
                            charts_and_stats,
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