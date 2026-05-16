import flet as ft
from src.models import *


def login_view(page):

    def func_for_show_modal_menu(e):
        pass


    async def go_home(e):
        await page.push_route("/")


    async def go_register(e):
        await page.push_route("/register")


    text_field_email = ft.TextField(
        label="Введіть ваш email",
        text_style=style_for_tf_text_reg_page,
        border_color=ft.Colors.RED_500,
        label_style=style_for_tf_label_reg_page,
        margin = 10,
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


    btn_login = ft.Button(
        "Увійти",
        style = style_for_default_btn,
        width = 200,
    )


    text_btn_register = ft.TextButton(
        ft.Text("Створити обліковий запис", size = 17, weight = ft.FontWeight.W_100),
        style = style_for_text_btn_reg_page,
        margin = 20,
        on_click = go_register
    )

    bottom_bar = ft.BottomAppBar(
    bgcolor=ft.Colors.ORANGE_900,
    content=ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            ft.IconButton(ft.Icons.MENU, on_click = func_for_show_modal_menu),
            ft.IconButton(ft.Icons.HOME, on_click = go_home),
            ft.IconButton(ft.Icons.SETTINGS),
        ],
    ),
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
            automatically_imply_leading=False
        ),
        bgcolor=ft.Colors.ORANGE_900,
        padding=15,
    )

    register_container = ft.Container(
        content=ft.Column(
            controls=[
                text_top_login := ft.Text(
                    "Увійти",
                    size=28,
                    color=ft.Colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                ),
                text_field_email,
                text_field_password,
                btn_login,
                ft.Container(expand = True,),
                text_btn_register,
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
        bottom_appbar = bottom_bar,
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        app_bar,
                        ft.Row(
                            controls=[register_container],
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Container(expand = True,),
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