import flet as ft
from src.models import *


def register_view(page):



    async def go_home(e):
        await page.push_route("/")

    async def go_login(e):
        await page.push_route("/login")

    text_field_email = ft.TextField(
        label="Введіть ваш email",
        text_style=style_for_tf_text_reg_page,
        border_color=ft.Colors.RED_500,
        label_style=style_for_tf_label_reg_page,
        margin=10,
    )
    text_field_name = ft.TextField(
        label="Введіть ваше ім'я",
        text_style=style_for_tf_text_reg_page,
        border_color=ft.Colors.RED_500,
        label_style=style_for_tf_label_reg_page,
        margin=10,
    )

    text_field_password = ft.TextField(
        label="Введіть пароль",
        text_style=style_for_tf_text_reg_page,
        border_color=ft.Colors.RED_500,
        label_style=style_for_tf_label_reg_page,
        password=True,
        can_reveal_password=True,
        margin=10,
    )

    text_field_confirm_password = ft.TextField(
        label="Підтвердіть пароль",
        text_style=style_for_tf_text_reg_page,
        border_color=ft.Colors.RED_500,
        label_style=style_for_tf_label_reg_page,
        password=True,
        can_reveal_password=True,
        margin=10,
    )

    btn_register = ft.Button(
        "Зареєструватися",
        style=style_for_default_btn,
        width=200,
    )

    text_btn_login = ft.TextButton(
        ft.Text("Увійти", size=17, weight=ft.FontWeight.W_100),
        style=style_for_text_btn_reg_page,
        margin=20,
        on_click=go_login
    )

    app_bar = ft.Container(
        content=ft.AppBar(
            title=ft.Text("Вхід"),
            actions=[
                ft.IconButton(
                    ft.Icons.HOME,
                    on_click=go_home,
                )
            ],
            bgcolor=ft.Colors.ORANGE_900,
            automatically_imply_leading = False
        ),
        bgcolor=ft.Colors.ORANGE_900,
        padding=15,
    )

    register_card = ft.Container(
        content=ft.Column(
            controls=[
                text_top_login := ft.Text(
                    "Реєстрація",
                    size=28,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
                text_field_name,
                text_field_email,
                text_field_password,
                text_field_confirm_password,
                btn_register,
                ft.Container(expand=True, ),
                text_btn_login,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        ),
        bgcolor=ft.Colors.YELLOW_700,
        width=700,
        height=500,
        alignment=ft.Alignment.CENTER,
        border_radius=20,
        opacity=0.9,
        padding=20,
    )

    return ft.View(
        route="/login",
        padding = 0,
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        app_bar,
                        ft.Row(
                            controls=[register_card],
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                bgcolor=ft.Colors.RED_800,
                expand=True,
            )
        ],
    )