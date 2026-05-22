import flet as ft
from src.models import *


def login_view(page):


    async def go_register(e):
        await page.push_route("/register")

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


    text_field_email = ft.TextField(
        label="Email",
        hint_text="your@email.com",
        text_style=style_for_tf_text_reg_page,
        border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        focused_border_color=ft.Colors.ORANGE_400,
        label_style=style_for_tf_label_reg_page,
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border_radius=10,
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
    )

    text_field_password = ft.TextField(
        label="Пароль",
        text_style=style_for_tf_text_reg_page,
        border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
        focused_border_color=ft.Colors.ORANGE_400,
        label_style=style_for_tf_label_reg_page,
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border_radius=10,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
    )


    btn_login = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    "Увійти",
                    color=ft.Colors.WHITE,
                    size=16,
                    weight=ft.FontWeight.W_600,
                ),
                ft.Icon(ft.Icons.ARROW_FORWARD, color=ft.Colors.WHITE, size=18),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        bgcolor=ft.Colors.ORANGE_700,
        border_radius=10,
        padding=ft.Padding(left=0, right=0, top=16, bottom=16),
        on_click=lambda e: None,
    )


    divider_row = ft.Row(
        controls=[
            ft.Container(
                height=1,
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                expand=True,
            ),
            ft.Text(
                "або",
                color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE),
                size=13,
            ),
            ft.Container(
                height=1,
                bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                expand=True,
            ),
        ],
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


    login_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.SHOW_CHART,
                                    color=ft.Colors.ORANGE_400,
                                    size=24,
                                ),
                                ft.Text(
                                    "Finance Helper",
                                    color=ft.Colors.ORANGE_400,
                                    size=15,
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=6,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Вхід до акаунту",
                            color=ft.Colors.WHITE,
                            size=26,
                            weight=ft.FontWeight.W_700,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Text(
                            "Раді бачити тебе знову",
                            color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE),
                            size=14,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
                ft.Container(height=28),
                text_field_email,
                ft.Container(height=4),
                text_field_password,
                ft.Container(height=4),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "Забули пароль?",
                                color=ft.Colors.ORANGE_300,
                                size=13,
                            ),
                            border_radius=4,
                            padding=ft.Padding(left=4, right=4, top=2, bottom=2),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Container(height=20),
                btn_login,
                ft.Container(height=20),
                divider_row,
                ft.Container(height=16),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Ще немає акаунту?",
                            color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE),
                            size=14,
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Створити",
                                color=ft.Colors.ORANGE_400,
                                size=14,
                                weight=ft.FontWeight.W_600,
                            ),
                            border_radius=4,
                            padding=ft.Padding(left=4, right=4, top=2, bottom=2),
                            on_click=go_register,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=6,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=0,
        ),
        bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
        border_radius=20,
        padding=36,
        width=460,
    )


    custom_appbar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.IconButton(
                            ft.Icons.ARROW_BACK_IOS_NEW,
                            icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                            icon_size=18,
                            on_click=go_home,
                            tooltip="Назад",
                        ),
                        ft.Icon(ft.Icons.SHOW_CHART, color=ft.Colors.ORANGE_300, size=20),
                        ft.Text(
                            "Finance Helper",
                            color=ft.Colors.WHITE,
                            size=18,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=6,
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
        padding=ft.Padding(left=8, right=8, top=0, bottom=0),
        border=ft.Border(
            bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE))
        ),
    )

    return ft.View(
        route="/login",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=login_card,
                                alignment=ft.Alignment.CENTER,
                                expand=True,
                                padding=ft.Padding(left=20, right=20, top=40, bottom=40),
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        ],
    )