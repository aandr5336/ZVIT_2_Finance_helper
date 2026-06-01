import flet as ft


def open_settings_dialog(page):
    def close(e):
        page.pop_dialog()

    def do_logout(e):
        from src.models.auth import logout_user
        page.pop_dialog()
        logout_user()
        import asyncio
        asyncio.ensure_future(page.push_route("/"))

    dlg = ft.AlertDialog(
        bgcolor=ft.Colors.with_opacity(0, ft.Colors.BLACK),
        alignment=ft.Alignment.CENTER,
        content=ft.Container(
            content=ft.Column(
                tight=True,
                spacing=0,
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.SETTINGS_OUTLINED, color=ft.Colors.ORANGE_400, size=22),
                                    bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_400),
                                    border_radius=10,
                                    padding=10,
                                    width=44,
                                    height=44,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Налаштування", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                                        ft.Text("Керування акаунтом", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=12),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.IconButton(ft.Icons.CLOSE, icon_color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), icon_size=18, on_click=close),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.Padding(left=20, right=8, top=20, bottom=16),
                    ),
                    ft.Container(height=1, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), margin=ft.Margin.only(left=20, right=20, bottom=16)),
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED_400, size=20),
                                                bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.RED_400),
                                                border_radius=8,
                                                padding=8,
                                                width=36,
                                                height=36,
                                            ),
                                            ft.Text("Вийти з акаунту", color=ft.Colors.RED_400, size=15, weight=ft.FontWeight.W_500, expand=True),
                                            ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE), size=18),
                                        ],
                                        spacing=14,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.RED_400),
                                    border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.RED_400)),
                                    border_radius=10,
                                    padding=ft.Padding(left=14, right=14, top=12, bottom=12),
                                    ink=True,
                                    on_click=do_logout,
                                ),
                            ],
                            spacing=8,
                        ),
                        padding=ft.Padding(left=16, right=16, top=0, bottom=20),
                    ),
                ],
            ),
            bgcolor=ft.Colors.GREY_900,
            border=ft.Border.all(1, ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
            border_radius=20,
            width=320,
        ),
    )
    page.show_dialog(dlg)


def open_left_menu_dialog(page, go_home, go_control_panel, go_transactions,
                           go_budget, go_goals, go_reports, go_categories, go_settings):
    def close(e):
        page.pop_dialog()

    items = [
        (ft.Icons.HOME_OUTLINED, "Головна", "Повернутись на головну", go_home),
        (ft.Icons.DASHBOARD_OUTLINED, "Панель керування", "Огляд фінансів", go_control_panel),
        (ft.Icons.SWAP_HORIZ, "Транзакції", "Всі операції", go_transactions),
        (ft.Icons.PIE_CHART_OUTLINE, "Бюджет", "Планування витрат", go_budget),
        (ft.Icons.FLAG_OUTLINED, "Цілі", "Фінансові цілі", go_goals),
        (ft.Icons.BAR_CHART_OUTLINED, "Звіти", "Аналітика та статистика", go_reports),
        (ft.Icons.CATEGORY_OUTLINED, "Категорії", "Управління категоріями", go_categories),
        (ft.Icons.SETTINGS_OUTLINED, "Налаштування", "Параметри акаунту", go_settings),
    ]

    def menu_item(icon, label, subtitle, on_click):
        return ft.Button(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=ft.Colors.ORANGE_400, size=18),
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_400),
                        border_radius=8,
                        padding=8,
                        width=36,
                        height=36,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(label, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_500),
                            ft.Text(subtitle, color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=11),
                        ],
                        spacing=1,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.with_opacity(0.25, ft.Colors.WHITE), size=16),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            style=ft.ButtonStyle(padding=ft.Padding(left=12, right=12, top=10, bottom=10)),
            on_click=on_click,
        )

    nav_items = [menu_item(icon, label, subtitle, event) for icon, label, subtitle, event in items]

    dlg = ft.AlertDialog(
        bgcolor=ft.Colors.with_opacity(0, ft.Colors.BLACK),
        alignment=ft.Alignment.TOP_LEFT,
        content=ft.Container(
            content=ft.Column(
                tight=True,
                spacing=0,
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.ORANGE_400, size=24),
                                    bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_400),
                                    border_radius=22,
                                    width=44,
                                    height=44,
                                ),
                                ft.Column(
                                    controls=[
                                        ft.Text("Finance Helper", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.W_700),
                                        ft.Text("Навігація", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=12),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.IconButton(ft.Icons.CLOSE, icon_color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), icon_size=18, on_click=close),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.Padding(left=20, right=8, top=20, bottom=16),
                    ),
                    ft.Container(height=1, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE), margin=ft.Margin.only(left=20, right=20, bottom=12)),
                    ft.Container(
                        content=ft.Column(controls=nav_items, spacing=6, scroll=ft.ScrollMode.AUTO),
                        padding=ft.Padding(left=16, right=16, top=0, bottom=20),
                        height=420,
                    ),
                ],
            ),
            bgcolor=ft.Colors.GREY_900,
            border=ft.Border.all(1, ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
            border_radius=20,
            width=340,
        ),
    )
    page.show_dialog(dlg)
