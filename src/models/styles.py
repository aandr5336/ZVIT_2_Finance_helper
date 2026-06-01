import flet as ft

style_for_main_big_text_main_page = ft.TextStyle(
    size=60,
    color=ft.Colors.WHITE,
    weight=ft.FontWeight.W_400,
    font_family="Nunito-Sans",
)

gradient_for_appbar = ft.RadialGradient(
    center=ft.Alignment.CENTER_LEFT,
    radius=15,
    colors=[ft.Colors.ORANGE_700, ft.Colors.ORANGE_500],
    stops=[0.0, 1.0],
)

style_for_tf_text_reg_page = ft.TextStyle(
    size=15,
    weight=ft.FontWeight.W_800,
    color=ft.Colors.WHITE,
)

style_for_text_btn_reg_page = ft.ButtonStyle(
    color=ft.Colors.WHITE,
    text_style=style_for_tf_text_reg_page,
)

style_for_tf_label_reg_page = ft.TextStyle(
    size=15,
    weight=ft.FontWeight.W_100,
    color=ft.Colors.WHITE,
)

style_for_default_btn = ft.ButtonStyle(
    color=ft.Colors.WHITE,
    bgcolor=ft.Colors.ORANGE_900,
    overlay_color=ft.Colors.RED_700,
    shape=ft.BeveledRectangleBorder(radius=15),
)

style_for_big_login_btn = ft.ButtonStyle(
    color=ft.Colors.WHITE,
    bgcolor=ft.Colors.ORANGE_900,
    overlay_color=ft.Colors.RED_700,
    text_style=ft.TextStyle(size=40),
    shape=ft.BeveledRectangleBorder(radius=100),
)


def card_maker(icon, title, desc):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Icon(icon, color=ft.Colors.ORANGE_400, size=28),
                    bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_400),
                    border_radius=12,
                    padding=12,
                    width=52,
                    height=52,
                ),
                ft.Text(title, color=ft.Colors.WHITE, size=15, weight=ft.FontWeight.W_600),
                ft.Text(desc, color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE), size=13),
            ],
            spacing=12,
        ),
        bgcolor=ft.Colors.with_opacity(0.07, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
        border_radius=16,
        padding=24,
        expand=True,
    )
