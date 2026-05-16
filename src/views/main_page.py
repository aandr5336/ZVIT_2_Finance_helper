import flet as ft
from src.models import *

def home_view(page):


    async def open_register(e):
        await page.push_route("/login")

    main_bg_gradient = ft.Container(
        gradient = ft.RadialGradient(
                            center=ft.Alignment.CENTER,
                            radius=1.3,
                            colors=[ft.Colors.YELLOW_700, ft.Colors.ORANGE_900,],
                            stops=[0.0, 1.0],
        ),
        expand=True,
        height = 1000,
        alignment = ft.Alignment.CENTER
    )

    app_bar = ft.Container(
        content=ft.AppBar(
            title=ft.Text("Finance helper"),
            actions=[
                ft.IconButton(
                    ft.Icons.SETTINGS,
                    on_click=open_register,
                )
            ],
            bgcolor=ft.Colors.ORANGE_900,
            automatically_imply_leading=False
        ),
        bgcolor=ft.Colors.ORANGE_900,
        padding=15,
    )

    return ft.View(
        route="/",
        padding = 0,
        scroll=ft.ScrollMode.ADAPTIVE,
        bgcolor =ft.Colors.ORANGE_900 ,
        controls=[ft.Column([
                app_bar,
                main_bg_gradient,
            ]
            )
        ]
    )