import flet as ft


def show_snack(page: ft.Page, message: str, success: bool = True):
    page.show_dialog(
        ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.GREEN_800 if success else ft.Colors.RED_800,
            duration=3000,
        )
    )


def show_confirm_dialog(page, title: str, message: str, on_confirm, confirm_label: str = "Підтвердити", danger: bool = False):
    def confirm(e):
        page.pop_dialog()
        on_confirm()

    def cancel(e):
        page.pop_dialog()

    dlg = ft.AlertDialog(
        bgcolor="#1a1a1a",
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                    ft.Container(height=8),
                    ft.Text(message, color=ft.Colors.with_opacity(0.65, ft.Colors.WHITE), size=14),
                    ft.Container(height=20),
                    ft.Row(
                        controls=[
                            ft.OutlinedButton(
                                "Скасувати",
                                style=ft.ButtonStyle(
                                    color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
                                    side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=cancel,
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                confirm_label,
                                bgcolor=ft.Colors.RED_700 if danger else ft.Colors.ORANGE_700,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0),
                                on_click=confirm,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                    ),
                ],
                tight=True,
                spacing=0,
            ),
            width=300,
            padding=20,
        ),
    )
    page.show_dialog(dlg)


async def navigate(page, route: str):
    try:
        page.pop_dialog()
    except Exception:
        pass
    await page.push_route(route)
