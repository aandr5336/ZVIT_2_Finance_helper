import flet as ft
from src.models import *
from src.storage import Session
from src.storage.session import Currency


def settings_view(page):

    async def go_home(e):
        await page.push_route("/")

    async def go_control_panel(e):
        page.pop_dialog()
        await page.push_route("/control_panel")

    async def go_transactions(e):
        page.pop_dialog()
        await page.push_route("/transactions")

    async def go_budget(e):
        page.pop_dialog()
        await page.push_route("/budget")

    async def go_goals(e):
        page.pop_dialog()
        await page.push_route("/goals")

    async def go_reports(e):
        page.pop_dialog()
        await page.push_route("/reports")

    async def go_categories(e):
        page.pop_dialog()
        await page.push_route("/categories")

    async def go_settings(e):
        page.pop_dialog()
        page.show_dialog(ft.SnackBar(ft.Text("Ви зараз на сторінці налаштувань.", color=ft.Colors.WHITE), bgcolor=ft.Colors.ORANGE_600))

    custom_appbar = ft.Container(
        content=ft.Row(controls=[
            ft.Row(controls=[
                ft.Icon(ft.Icons.SHOW_CHART, color=ft.Colors.ORANGE_300, size=20),
                ft.Text("Finance Helper", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.W_600),
            ], spacing=8, expand=True),
            ft.IconButton(ft.Icons.MENU, icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE), icon_size=20,
                          on_click=lambda e: open_left_menu_dialog(page, go_home, go_control_panel, go_transactions, go_budget, go_goals, go_reports, go_categories, go_settings)),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        gradient=gradient_for_appbar, height=60,
        padding=ft.Padding(left=20, right=8, top=0, bottom=0),
        border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE))),
    )

    def setting_row(icon, label, subtitle=None, trailing=None, color=ft.Colors.ORANGE_400, on_click=None):
        return ft.Container(
            content=ft.Row(controls=[
                ft.Container(content=ft.Icon(icon, color=color, size=18), bgcolor=ft.Colors.with_opacity(0.1, color), border_radius=8, padding=8, width=36, height=36),
                ft.Column(controls=[
                    ft.Text(label, color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_500),
                    ft.Text(subtitle, color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=12) if subtitle else ft.Container(),
                ], spacing=1, expand=True),
                trailing if trailing else ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.with_opacity(0.25, ft.Colors.WHITE), size=18),
            ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.07, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=14, right=10, top=12, bottom=12),
            on_click=on_click,
            height = 60
        )

    def section_title(title):
        return ft.Container(
            content=ft.Text(title, color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=12, weight=ft.FontWeight.W_600, style = ft.TextStyle(letter_spacing=0.8)),
            padding=ft.Padding(left=4, right=0, top=0, bottom=4),
        )

    async def fetch_usd_rate() -> float:
        import urllib.request
        import json
        try:
            url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read())
            for item in data:
                if item.get("ccy") == "USD":
                    rate = float(item["sale"])
                    from src.storage.session import Currency
                    Currency.set_rate(rate)
                    return rate
        except Exception:
            pass
        return 41.0

    def open_change_password(e):
        tf_old = ft.TextField(label="Старий пароль", password=True, can_reveal_password=True, border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
        tf_new = ft.TextField(label="Новий пароль", password=True, can_reveal_password=True, border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
        tf_confirm = ft.TextField(label="Підтвердіть пароль", password=True, can_reveal_password=True, border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)

        def do_change(ev):
            ok, msg = change_password(tf_old.value or "", tf_new.value or "", tf_confirm.value or "")
            page.pop_dialog()
            show_snack(page, msg, success=ok)

        dlg = ft.AlertDialog(
            bgcolor="#1a1a1a",
            content=ft.Container(content=ft.Column(controls=[
                ft.Text("Змінити пароль", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                ft.Container(height=16),
                tf_old,
                ft.Container(height=8),
                tf_new,
                ft.Container(height=8),
                tf_confirm,
                ft.Container(height=16),
                ft.Row(controls=[
                    ft.OutlinedButton("Скасувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: page.pop_dialog(), expand=True),
                    ft.Button("Зберегти", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0), on_click=do_change, expand=True),
                ], spacing=12),
            ], tight=True, spacing=0), width=320, padding=20),
        )
        page.show_dialog(dlg)

    async def do_logout(e):
        logout_user()
        await page.push_route("/")

    async def do_delete_account(e):
        from src.storage.json_store import _read, _write
        db = _read()
        db["users"] = [u for u in db["users"] if u["id"] != Session.user_id()]
        _write(db)
        logout_user()
        show_snack(page, "Акаунт видалено")
        await page.push_route("/")

    def confirm_logout(e):
        show_confirm_dialog(page, "Вийти?", "Ви впевнені що хочете вийти з акаунту?",
                            lambda: page.run_task(do_logout, None), "Вийти", danger=False)

    def confirm_delete(e):
        show_confirm_dialog(page, "Видалити акаунт?", "Всі ваші дані будуть видалені назавжди. Цю дію не можна скасувати.",
                            lambda: page.run_task(do_delete_account, None), "Видалити", danger=True)

    rate_text = ft.Text("", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=12)

    async def load_rate_and_show():
        rate = await fetch_usd_rate()
        rate_text.value = f"Курс: 1 USD = {rate:.2f} ₴"
        page.update()

    def open_currency_dialog(e):
        page.run_task(load_rate_and_show)

        def select_uah(ev):
            check_icon_for_grn.opacity = 1
            check_icon_for_dollar.opacity = 0
            Currency.set("UAH")
            page.update()

        def select_usd(ev):
            check_icon_for_grn.opacity = 0
            check_icon_for_dollar.opacity = 1
            Currency.set("USD")
            page.update()

        def close_and_refresh(ev):
            page.pop_dialog()
            import asyncio
            asyncio.ensure_future(page.push_route("/settings"))

        current = "Гривня (₴)" if Currency.get() == "UAH" else "Долар ($)"

        dlg = ft.AlertDialog(
            bgcolor="#1a1a1a",
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Text("Валюта", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                    ft.Container(height=4),
                    rate_text,
                    ft.Container(height=16),
                    ft.Container(
                        content=ft.Row(controls=[
                            ft.Icon(ft.Icons.ATTACH_MONEY, color=ft.Colors.GREEN_400, size=20),
                            ft.Text("Гривня (₴)", color=ft.Colors.WHITE, size=15, expand=True),
                            check_icon_for_grn := ft.Icon(ft.Icons.CHECK, color=ft.Colors.ORANGE_400,
                                    size=18),
                        ], spacing=12),
                        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
                        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.ORANGE_400)),
                        border_radius=10,
                        padding=ft.Padding(left=14, right=14, top=12, bottom=12),
                        on_click=select_uah,
                    ),
                    ft.Container(height=8),
                    ft.Container(
                        content=ft.Row(controls=[
                            ft.Icon(ft.Icons.ATTACH_MONEY, color=ft.Colors.GREEN_400, size=20),
                            ft.Text("Долар ($)", color=ft.Colors.WHITE, size=15, expand=True),
                            check_icon_for_dollar := ft.Icon(ft.Icons.CHECK, color=ft.Colors.ORANGE_400, size=18, opacity = 0),
                        ], spacing=12),
                        bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
                        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.ORANGE_400)),
                        border_radius=10,
                        padding=ft.Padding(left=14, right=14, top=12, bottom=12),
                        on_click=select_usd,
                    ),
                    ft.Container(height=20),
                    ft.Button(
                        "Готово",
                        bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0),
                        on_click=close_and_refresh,
                        height = 30
                    ),
                ], tight=True, spacing=0),
                width=300, padding=20,
            ),
        )
        page.show_dialog(dlg)

    profile_card = ft.Container(
        content=ft.Row(controls=[
            ft.Container(content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.ORANGE_400, size=32), bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_400), border_radius=30, width=60, height=60),
            ft.Column(controls=[
                ft.Text(Session.user_name(), color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                ft.Text(Session.user_email(), color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=13),
            ], spacing=4, expand=True),
        ], spacing=16, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.with_opacity(0.18, ft.Colors.ORANGE_700), ft.Colors.with_opacity(0.08, ft.Colors.WHITE)]),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.ORANGE_400)),
        border_radius=16, padding=20,
        margin=ft.Margin.symmetric(horizontal=20, vertical=8),
    )

    content = ft.Container(
        content=ft.Column(controls=[
            ft.Column(controls=[section_title("ЗАГАЛЬНІ НАЛАШТУВАННЯ"), ft.Column(controls=[
                setting_row(ft.Icons.LOCK_OUTLINE, "Змінити пароль", None, on_click=open_change_password),
                setting_row(ft.Icons.LOGOUT, "Вийти з акаунту", None, on_click=confirm_logout),
                setting_row(ft.Icons.DELETE_FOREVER_OUTLINED, "Видалити акаунт", "Незворотня дія", on_click=confirm_delete),
                setting_row(ft.Icons.ATTACH_MONEY_OUTLINED, "Валюта", f"Поточна: {'Гривня (₴)' if Currency.get() == 'UAH' else 'Долар ($)'}", on_click=open_currency_dialog,
                ),

            ], spacing=8)], spacing=8),
        ], spacing=24),
        padding=ft.Padding(left=20, right=20, top=8, bottom=32),
    )

    return ft.View(
        route="/settings",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(controls=[
                custom_appbar,
                ft.Column(controls=[profile_card, content], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0),
            ], spacing=0, expand=True),
        ],
    )
