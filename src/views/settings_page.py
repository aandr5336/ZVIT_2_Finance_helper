import flet as ft
from src.models import *
from src.assets import *


def settings_view(page):


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
        await page.push_route("/categories")


    async def go_settings(e):
        page.pop_dialog()
        page.show_dialog(
            ft.SnackBar(
                ft.Text("Ви зараз на сторінці налаштувань.", color = ft.Colors.WHITE),
                bgcolor = ft.Colors.ORANGE_600,
            )
        )



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


    profile_card = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.ORANGE_400, size=32),
                    bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_400),
                    border_radius=30,
                    width=60,
                    height=60,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "Олексій Коваленко",
                            color=ft.Colors.WHITE,
                            size=17,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "oleksii@email.com",
                            color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                            size=13,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Pro акаунт",
                                color=ft.Colors.ORANGE_300,
                                size=11,
                                weight=ft.FontWeight.W_600,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_300),
                            border_radius=6,
                            padding=ft.Padding(left=8, right=8, top=3, bottom=3),
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
                ft.IconButton(
                    ft.Icons.EDIT_OUTLINED,
                    icon_color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                    icon_size=20,
                    on_click=lambda e: None,
                ),
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
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


    def section_title(title):
        return ft.Container(
            content=ft.Text(
                title,
                color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                size=12,
                weight=ft.FontWeight.W_600,
                style = ft.TextStyle(letter_spacing=0.8),
            ),
            padding=ft.Padding(left=4, right=0, top=0, bottom=4),
        )


    def setting_row(icon, label, subtitle=None, trailing=None, color=ft.Colors.ORANGE_400, on_click=None):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=color, size=18),
                        bgcolor=ft.Colors.with_opacity(0.1, color),
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
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                subtitle,
                                color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                                size=12,
                            ) if subtitle else ft.Container(),
                        ],
                        spacing=1,
                        expand=True,
                    ),
                    trailing if trailing else ft.Icon(
                        ft.Icons.CHEVRON_RIGHT,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.WHITE),
                        size=18,
                    ),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.07, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=14, right=10, top=12, bottom=12),
            ink=True if on_click else False,
            on_click=on_click,
        )

    def setting_group(title, rows):
        return ft.Column(
            controls=[
                section_title(title),
                ft.Column(controls=rows, spacing=8),
            ],
            spacing=8,
        )


    dark_mode_switch = ft.Switch(
        value=True,
        active_color=ft.Colors.ORANGE_500,
        inactive_thumb_color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
        inactive_track_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
    )



    content = ft.Container(
        content=ft.Column(
            controls=[
                setting_group("ЗАГАЛЬНІ", [
                    setting_row(
                        ft.Icons.ATTACH_MONEY_OUTLINED,
                        "Валюта",
                        "Гривня (₴)",
                        on_click=lambda e: None,
                    ),
                    setting_row(
                        ft.Icons.CALENDAR_TODAY_OUTLINED,
                        "Початок місяця",
                        "1-е число",
                        on_click=lambda e: None,
                    ),
                    setting_row(
                        ft.Icons.DARK_MODE_OUTLINED,
                        "Темна тема",
                        "Увімкнено",
                        trailing=dark_mode_switch,
                    ),
                    setting_row(
                        ft.Icons.ALARM_OUTLINED,
                        "Нагадування про бюджет",
                        "При 80% витрат",
                        on_click=lambda e: None,
                    ),
                ]),


                setting_group("БЕЗПЕКА", [
                    setting_row(
                        ft.Icons.LOCK_OUTLINE,
                        "Змінити пароль",
                        None,
                        on_click=lambda e: None,
                    ),
                    setting_row(
                        ft.Icons.LOGOUT,
                        "Вийти з акаунту",
                        None,
                        on_click=lambda e: None,
                    ),
                    setting_row(
                        icon=ft.Icons.DELETE_FOREVER_OUTLINED,
                        label="Видалити акаунт",
                        subtitle="Незворотня дія",
                        on_click=lambda e: None,
                    ),
                ]),


            ],
            spacing=24,
        ),
        padding=ft.Padding(left=20, right=20, top=8, bottom=32),
    )

    return ft.View(
        route="/settings",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            profile_card,
                            content,
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