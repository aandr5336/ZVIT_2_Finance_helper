import flet as ft
from flet import Dropdown

from src.models import *


def budget_view(page):

    state = {"month": current_month()}

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
        page.show_dialog(ft.SnackBar(ft.Text("Ви зараз на сторінці бюджету.", color=ft.Colors.WHITE), bgcolor=ft.Colors.ORANGE_600))

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
        await page.push_route("/settings")

    custom_appbar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SHOW_CHART, color=ft.Colors.ORANGE_300, size=20),
                        ft.Text("Finance Helper", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.W_600),
                    ],
                    spacing=8,
                    expand=True,
                ),
                ft.IconButton(ft.Icons.SETTINGS_OUTLINED, icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE), icon_size=20, on_click=lambda e: open_settings_dialog(page)),
                ft.IconButton(ft.Icons.MENU, icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE), icon_size=20,
                              on_click=lambda e: open_left_menu_dialog(page, go_home, go_control_panel, go_transactions, go_budget, go_goals, go_reports, go_categories, go_settings)),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        gradient=gradient_for_appbar,
        height=60,
        padding=ft.Padding(left=20, right=8, top=0, bottom=0),
        border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE))),
    )

    month_label = ft.Text("", color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_600, expand=True, text_align=ft.TextAlign.CENTER)
    overall_text = ft.Text("", color=ft.Colors.WHITE, size=24, weight=ft.FontWeight.W_700)
    overall_pct = ft.Text("", color=ft.Colors.ORANGE_300, size=22, weight=ft.FontWeight.W_700)
    overall_remaining = ft.Text("", color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE), size=12)
    budgets_column = ft.Column(spacing=10)

    def refresh():
        m = state["month"]
        month_label.value = format_month_label(m)
        prog = get_total_budget_progress(m)
        overall_text.value = f"₴ {prog['total_spent']:,.0f} / ₴ {prog['total_budget']:,.0f}".replace(",", " ")
        overall_pct.value = f"{int(prog['percent'] * 100)}%"
        overall_remaining.value = f"Залишилось ₴ {prog['remaining']:,.0f}".replace(",", " ")

        budgets = get_budgets_with_progress(m)
        budgets_column.controls.clear()
        if not budgets:
            budgets_column.controls.append(
                ft.Container(
                    content=ft.Text("Бюджетів немає. Натисніть '+ Бюджет' щоб додати.", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=14, text_align=ft.TextAlign.CENTER),
                    padding=40, alignment=ft.Alignment.CENTER,
                )
            )
        for b in budgets:
            percent = b["percent"]
            is_over = b["is_over"]
            bar_color = ft.Colors.RED_400 if is_over else ft.Colors.ORANGE_400

            def make_edit(budget_id, current_amount):
                def do_edit(e):
                    tf = ft.TextField(
                        label="Сума бюджету (₴)",
                        value=str(current_amount),
                        keyboard_type=ft.KeyboardType.NUMBER,
                        border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                        focused_border_color=ft.Colors.ORANGE_400,
                        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                        color=ft.Colors.WHITE,
                        label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
                        border_radius=10,
                    )
                    def save(e):
                        try:
                            amt = float(tf.value.replace(",", "."))
                        except (ValueError, AttributeError):
                            show_snack(page, "Введіть коректну суму", success=False)
                            return
                        from src.storage.json_store import _read, _write
                        db = _read()
                        from src.storage import Session
                        for u in db["users"]:
                            if u["id"] == Session.user_id():
                                for bgt in u["budgets"]:
                                    if bgt["id"] == budget_id:
                                        bgt["amount"] = amt
                                        break
                                break
                        _write(db)
                        page.pop_dialog()
                        show_snack(page, "Бюджет оновлено")
                        refresh()
                        page.update()

                    dlg = ft.AlertDialog(
                        bgcolor="#1a1a1a",
                        content=ft.Container(
                            content=ft.Column(controls=[
                                ft.Text("Редагувати бюджет", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                                ft.Container(height=16),
                                tf,
                                ft.Container(height=16),
                                ft.Row(controls=[
                                    ft.OutlinedButton("Скасувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: page.pop_dialog(), expand=True),
                                    ft.Button("Зберегти", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0), on_click=save, expand=True),
                                ], spacing=12),
                            ], tight=True, spacing=0),
                            width=300, padding=20,
                        ),
                    )
                    page.show_dialog(dlg)
                return do_edit

            def make_delete(budget_id):
                def do_delete(e):
                    delete_budget(budget_id)
                    show_snack(page, "Бюджет видалено")
                    refresh()
                    page.update()
                return do_delete

            budgets_column.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(b["category"], color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_600),
                                            ft.Text("Перевищено!" if is_over else f"Залишилось ₴{b['remaining']:,.0f}".replace(",", " "),
                                                    color=ft.Colors.RED_400 if is_over else ft.Colors.GREEN_400, size=11),
                                        ],
                                        spacing=2,
                                        expand=True,
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(f"₴{b['spent']:,.0f}".replace(",", " "), color=ft.Colors.WHITE, size=15, weight=ft.FontWeight.W_700),
                                            ft.Text(f"з ₴{b['amount']:,.0f}".replace(",", " "), color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=11),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                        spacing=2,
                                    ),
                                ],
                                spacing=12,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Container(height=10),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                                        border_radius=4, height=6, expand=True,
                                        content=ft.Row(controls=[
                                            ft.Container(bgcolor=bar_color, border_radius=4, height=6,
                                                         expand=int(percent * 100) or 1),
                                            ft.Container(expand=max(100 - int(percent * 100),
                                                                    0)) if percent < 1.0 else ft.Container(width=0),
                                        ], spacing=0, expand=True),
                                    ),
                                ], expand=True,
                            ),
                            ft.Container(height=2),
                            ft.Row(
                                controls=[
                                    ft.Text(f"{int(percent * 100)}% використано", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=11),
                                    ft.Row(controls=[
                                        ft.TextButton("Редагувати", style=ft.ButtonStyle(color=ft.Colors.ORANGE_400, padding=ft.Padding(left=0, right=8, top=0, bottom=0)), on_click=make_edit(b["id"], b["amount"])),
                                        ft.TextButton("Видалити", style=ft.ButtonStyle(color=ft.Colors.RED_400, padding=ft.Padding(left=0, right=0, top=0, bottom=0)), on_click=make_delete(b["id"])),
                                    ], spacing=0),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=0,
                    ),
                    bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
                    border_radius=14,
                    padding=16,
                )
            )
        page.update()

    refresh()

    def prev_m(e):
        state["month"] = prev_month(state["month"])
        refresh()

    def next_m(e):
        state["month"] = next_month(state["month"])
        refresh()

    def open_add_budget(e):
        cats = get_categories(cat_type="expense")
        if not cats:
            show_snack(page, "Немає категорій витрат", success=False)
            return

        dd_cat = ft.Dropdown(
            label="Категорія",
            options=[ft.DropdownOption(str(c["id"]), c["name"]) for c in cats],
            value=str(cats[0]["id"]) if cats else None,
            border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            focused_border_color=ft.Colors.ORANGE_400,
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
            color=ft.Colors.WHITE,
            menu_height = 300,
            label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
        )
        tf_amount = ft.TextField(
            label="Сума бюджету (₴)",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            focused_border_color=ft.Colors.ORANGE_400,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
            border_radius=10,
        )

        def do_save(e):
            try:
                amt = float(tf_amount.value.replace(",", "."))
            except (ValueError, AttributeError):
                show_snack(page, "Введіть коректну суму", success=False)
                return
            if not dd_cat.value:
                show_snack(page, "Оберіть категорію", success=False)
                return
            ok, msg = set_budget(int(dd_cat.value), amt, state["month"])
            page.pop_dialog()
            show_snack(page, msg, success=ok)
            if ok:
                refresh()

        dlg = ft.AlertDialog(
            bgcolor="#1a1a1a",
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Text("Новий бюджет", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                    ft.Container(height=16),
                    dd_cat,
                    ft.Container(height=8),
                    tf_amount,
                    ft.Container(height=16),
                    ft.Row(controls=[
                        ft.OutlinedButton("Скасувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: page.pop_dialog(), expand=True),
                        ft.Button("Зберегти", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0), on_click=do_save, expand=True),
                    ], spacing=12),
                ], tight=True, spacing=0),
                width=300, padding=20,
            ),
        )
        page.show_dialog(dlg)

    overall_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(controls=[
                            ft.Text("Загальний бюджет", color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), size=13),
                            overall_text,
                        ], spacing=4, expand=True),
                        ft.Container(content=overall_pct, bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_300), border_radius=12, padding=ft.Padding(left=14, right=14, top=10, bottom=10)),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=12),
                ft.Row(controls=[
                    ft.Row(controls=[
                        ft.Container(width=8, height=8, bgcolor=ft.Colors.GREEN_400, border_radius=4),
                        overall_remaining,
                    ], spacing=6),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ],
            spacing=0,
        ),
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.with_opacity(0.18, ft.Colors.ORANGE_700), ft.Colors.with_opacity(0.08, ft.Colors.WHITE)]),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.ORANGE_400)),
        border_radius=16,
        padding=20,
        margin=ft.Margin.symmetric(horizontal=20, vertical=4),
    )

    month_switcher = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(ft.Icons.CHEVRON_LEFT, icon_color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), icon_size=20, on_click=prev_m),
                month_label,
                ft.IconButton(ft.Icons.CHEVRON_RIGHT, icon_color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), icon_size=20, on_click=next_m),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=10,
        margin=ft.Margin.symmetric(horizontal=20, vertical=8),
        padding=ft.Padding(left=4, right=4, top=4, bottom=4),
    )

    header_section = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(controls=[
                    ft.Text("Бюджет", color=ft.Colors.WHITE, size=22, weight=ft.FontWeight.W_700),
                    ft.Text(format_month_label(state["month"]), color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=13),
                ], spacing=3, expand=True),
                ft.Button("+ Бюджет", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE,
                          style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                          height=38, on_click=open_add_budget),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(left=20, right=20, top=20, bottom=12),
    )

    return ft.View(
        route="/budget",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            header_section,
                            overall_card,
                            month_switcher,
                            ft.Container(
                                content=ft.Column(controls=[
                                    ft.Text("Категорії бюджету", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.W_700),
                                    ft.Container(height=4),
                                    budgets_column,
                                ], spacing=10),
                                padding=ft.Padding(left=20, right=20, top=8, bottom=24),
                            ),
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
