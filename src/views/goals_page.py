import flet as ft
from src.models import *
from src.assets import *


def goals_view(page):


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
                            "Фінансові цілі",
                            color=ft.Colors.WHITE,
                            size=22,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "3 активні цілі",
                            color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                            size=13,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.Button(
                    "+ Ціль",
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


    def mini_stat(label, value, color):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        value,
                        color=color,
                        size=18,
                        weight=ft.FontWeight.W_700,
                    ),
                    ft.Text(
                        label,
                        color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                        size=11,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3,
            ),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=16, right=16, top=14, bottom=14),
            expand=True,
        )

    summary_row = ft.Container(
        content=ft.Row(
            controls=[
                mini_stat("Накопичено", "₴34 500", ft.Colors.GREEN_400),
                mini_stat("Залишилось", "₴65 500", ft.Colors.ORANGE_300),
                mini_stat("Виконано", "1 ціль", ft.Colors.BLUE_300),
            ],
            spacing=10,
        ),
        padding=ft.Padding(left=20, right=20, top=0, bottom=12),
    )


    def goal_card(icon, title, description, saved, total, color, deadline, is_done=False):
        percent = min(saved / total, 1.0)
        remaining = total - saved

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(icon, color=color, size=22),
                                bgcolor=ft.Colors.with_opacity(0.12, color),
                                border_radius=12,
                                padding=10,
                                width=44,
                                height=44,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        title,
                                        color=ft.Colors.WHITE,
                                        size=15,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    ft.Text(
                                        description,
                                        color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                                        size=12,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "✓ Виконано" if is_done else deadline,
                                    color=ft.Colors.GREEN_400 if is_done else ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                                    size=11,
                                    weight=ft.FontWeight.W_500,
                                ),
                                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400) if is_done else ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                                border_radius=6,
                                padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=14),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"₴{saved:,}",
                                color=ft.Colors.WHITE,
                                size=18,
                                weight=ft.FontWeight.W_700,
                            ),
                            ft.Text(
                                f"з ₴{total:,}",
                                color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                size=14,
                            ),
                        ],
                        spacing=6,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Container(height=8),
                    ft.Stack(
                        controls=[
                            ft.Container(
                                bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                                border_radius=6,
                                height=8,
                            ),
                            ft.Container(
                                gradient=ft.LinearGradient(
                                    begin=ft.Alignment(-1, 0),
                                    end=ft.Alignment(1, 0),
                                    colors=[color, ft.Colors.with_opacity(0.7, color)],
                                ),
                                border_radius=6,
                                height=8,
                                width=320 * percent,
                            ),
                        ],
                    ),
                    ft.Container(height=6),
                    ft.Row(
                        controls=[
                            ft.Text(
                                f"{int(percent * 100)}% виконано",
                                color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                size=11,
                            ),
                            ft.Row(
                                controls=[
                                    ft.TextButton(
                                        "Поповнити",
                                        style=ft.ButtonStyle(
                                            color=ft.Colors.ORANGE_400,
                                            padding=ft.Padding(left=0, right=8, top=0, bottom=0),
                                        ),
                                    ),
                                    ft.TextButton(
                                        "Редагувати",
                                        style=ft.ButtonStyle(
                                            color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                            padding=ft.Padding(left=0, right=0, top=0, bottom=0),
                                        ),
                                    ),
                                ],
                                spacing=0,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.1 if not is_done else 0.2, ft.Colors.GREEN_400 if is_done else ft.Colors.WHITE)),
            border_radius=16,
            padding=18,
            opacity=0.6 if is_done else 1.0,
        )


    def completed_goal_card(icon, title, total, color, completed_date):
        return ft.Container(
            content=ft.Row(
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
                            ft.Text(title, color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), size=14, weight=ft.FontWeight.W_500),
                            ft.Text(f"₴{total:,} • {completed_date}", color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE), size=12),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN_400, size=20),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.07, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=14, right=14, top=12, bottom=12),
        )

    goals_list = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Активні цілі",
                    color=ft.Colors.WHITE,
                    size=16,
                    weight=ft.FontWeight.W_700,
                ),
                ft.Container(height=4),
                goal_card(
                    ft.Icons.DIRECTIONS_CAR_OUTLINED,
                    "Новий автомобіль",
                    "Toyota Corolla 2024",
                    saved=45000,
                    total=600000,
                    color=ft.Colors.BLUE_400,
                    deadline="до груд. 2026",
                ),
                goal_card(
                    ft.Icons.BEACH_ACCESS_OUTLINED,
                    "Відпустка в Туреччині",
                    "Готель + переліт",
                    saved=18500,
                    total=25000,
                    color=ft.Colors.ORANGE_400,
                    deadline="до черв. 2025",
                ),
                goal_card(
                    ft.Icons.LAPTOP_OUTLINED,
                    "MacBook Pro",
                    "Apple M3 Pro 16\"",
                    saved=32000,
                    total=85000,
                    color=ft.Colors.PURPLE_300,
                    deadline="до верес. 2025",
                ),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Виконані цілі",
                            color=ft.Colors.WHITE,
                            size=16,
                            weight=ft.FontWeight.W_700,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=4),
                completed_goal_card(
                    ft.Icons.PHONE_IPHONE_OUTLINED,
                    "iPhone 15",
                    42000,
                    ft.Colors.GREEN_400,
                    "Березень 2025",
                ),
            ],
            spacing=12,
        ),
        padding=ft.Padding(left=20, right=20, top=4, bottom=24),
    )

    return ft.View(
        route="/goals",
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
                            goals_list,
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