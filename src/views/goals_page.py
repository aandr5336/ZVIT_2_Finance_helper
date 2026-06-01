import flet as ft
import datetime
from src.models import *


def goals_view(page):

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
        page.show_dialog(ft.SnackBar(ft.Text("Ви зараз на сторінці цілей.", color=ft.Colors.WHITE), bgcolor=ft.Colors.ORANGE_600))

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
                    spacing=8, expand=True,
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

    goals_column = ft.Column(spacing=12)
    summary_income = ft.Text("₴0", color=ft.Colors.GREEN_400, size=18, weight=ft.FontWeight.W_700)
    summary_remaining = ft.Text("₴0", color=ft.Colors.ORANGE_300, size=18, weight=ft.FontWeight.W_700)
    summary_done = ft.Text("0", color=ft.Colors.BLUE_300, size=18, weight=ft.FontWeight.W_700)

    def refresh():
        s = get_goals_summary()
        summary_income.value = format_currency(s["total_saved"])
        summary_remaining.value = format_currency(s["total_target"] - s["total_saved"])
        summary_done.value = str(s["done"])

        goals = get_goals()
        goals_column.controls.clear()

        active = [g for g in goals if not g["is_done"]]
        done = [g for g in goals if g["is_done"]]

        if not active and not done:
            goals_column.controls.append(
                ft.Container(
                    content=ft.Text("Цілей немає. Натисніть '+ Ціль' щоб додати.", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=14, text_align=ft.TextAlign.CENTER),
                    padding=40, alignment=ft.Alignment.CENTER,
                )
            )
        else:
            if active:
                goals_column.controls.append(ft.Text("Активні цілі", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.W_700))
                goals_column.controls.append(ft.Container(height=4))
                for g in active:
                    goals_column.controls.append(goal_card(g))

            if done:
                goals_column.controls.append(ft.Container(height=8))
                goals_column.controls.append(
                    ft.Row(controls=[
                        ft.Text("Виконані цілі", color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.W_700),
                    ])
                )
                goals_column.controls.append(ft.Container(height=4))
                for g in done:
                    goals_column.controls.append(done_card(g))

        page.update()

    def goal_card(g):
        percent = g["percent"]

        def open_add_savings(e):
            tf = ft.TextField(
                label="Сума поповнення (₴)",
                keyboard_type=ft.KeyboardType.NUMBER,
                border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                focused_border_color=ft.Colors.ORANGE_400,
                bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                color=ft.Colors.WHITE,
                label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
                border_radius=10,
            )
            def do_save(ev):
                try:
                    amt = float(tf.value.replace(",", "."))
                except (ValueError, AttributeError):
                    show_snack(page, "Введіть коректну суму", success=False)
                    return
                ok, msg = add_savings(g["id"], amt)
                page.pop_dialog()
                show_snack(page, msg, success=ok)
                if ok:
                    refresh()

            dlg = ft.AlertDialog(
                bgcolor="#1a1a1a",
                content=ft.Container(
                    content=ft.Column(controls=[
                        ft.Text(f"Поповнити: {g['title']}", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                        ft.Container(height=16),
                        tf,
                        ft.Container(height=16),
                        ft.Row(controls=[
                            ft.OutlinedButton("Скасувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: page.pop_dialog(), expand=True),
                            ft.Button("Поповнити", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0), on_click=do_save, expand=True),
                        ], spacing=12),
                    ], tight=True, spacing=0),
                    width=300, padding=20,
                ),
            )
            page.show_dialog(dlg)

        def open_edit(e):
            tf_title = ft.TextField(label="Назва", value=g["title"], border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
            tf_target = ft.TextField(label="Сума (₴)", value=str(g["target"]), keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
            tf_desc = ft.TextField(label="Опис", value=g.get("description", ""), border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)

            date_text = ft.Text(f"Дедлайн: {g.get('deadline') or 'не вказано'}", color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), size=13)
            chosen_deadline = {"value": g.get("deadline") or ""}

            def on_date_change(ev):
                chosen_deadline["value"] = ev.control.value.strftime("%Y-%m-%d") if ev.control.value else ""
                date_text.value = f"Дедлайн: {chosen_deadline['value'] or 'не вказано'}"
                page.update()

            def open_dp(ev):
                page.show_dialog(ft.DatePicker(
                    first_date=datetime.datetime(2020, 1, 1),
                    last_date=datetime.datetime(2035, 12, 31),
                    value=datetime.datetime.now(),
                    on_change=on_date_change,
                ))

            def do_save(ev):
                try:
                    target = float(tf_target.value.replace(",", "."))
                except (ValueError, AttributeError):
                    show_snack(page, "Введіть коректну суму", success=False)
                    return
                ok, msg = update_goal(g["id"], tf_title.value or "", target, tf_desc.value or "", chosen_deadline["value"])
                page.pop_dialog()
                show_snack(page, msg, success=ok)
                if ok:
                    refresh()

            dlg = ft.AlertDialog(
                bgcolor="#1a1a1a",
                content=ft.Container(
                    content=ft.Column(controls=[
                        ft.Text("Редагувати ціль", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                        ft.Container(height=16),
                        tf_title,
                        ft.Container(height=8),
                        tf_target,
                        ft.Container(height=8),
                        tf_desc,
                        ft.Container(height=8),
                        ft.Row(controls=[date_text, ft.IconButton(ft.Icons.CALENDAR_MONTH, icon_color=ft.Colors.ORANGE_400, icon_size=20, on_click=open_dp)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=16),
                        ft.Row(controls=[
                            ft.OutlinedButton("Скасувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: page.pop_dialog(), expand=True),
                            ft.Button("Зберегти", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0), on_click=do_save, expand=True),
                        ], spacing=12),
                    ], tight=True, spacing=0),
                    width=320, padding=20,
                ),
            )
            page.show_dialog(dlg)

        def do_delete(e):
            show_confirm_dialog(page, "Видалити ціль?", f"Ціль «{g['title']}» буде видалена.", lambda: (delete_goal(g["id"]), refresh()), "Видалити", danger=True)

        return ft.Container(
            content=ft.Column(controls=[
                ft.Row(controls=[
                    ft.Container(content=ft.Icon(ft.Icons.FLAG_OUTLINED, color=ft.Colors.ORANGE_400, size=22), bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ORANGE_400), border_radius=12, padding=10, width=44, height=44),
                    ft.Column(controls=[
                        ft.Text(g["title"], color=ft.Colors.WHITE, size=15, weight=ft.FontWeight.W_600),
                        ft.Text(g.get("description") or "", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=12),
                    ], spacing=2, expand=True),
                    ft.Container(
                        content=ft.Text(g.get("deadline") or "—", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=11),
                        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), border_radius=6,
                        padding=ft.Padding(left=8, right=8, top=4, bottom=4),
                    ),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=14),
                ft.Row(controls=[
                    ft.Text(format_currency(g["saved"]), color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.W_700),
                    ft.Text(f"з {format_currency(g['target'])}", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=14),
                ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.END),
                ft.Container(height=8),
                ft.Row(
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE),
                            border_radius=6, height=8, expand=True,
                            content=ft.Row(controls=[
                                ft.Container(
                                    gradient=ft.LinearGradient(begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0),
                                                               colors=[ft.Colors.ORANGE_700, ft.Colors.ORANGE_400]),
                                    border_radius=6, height=8, expand=int(percent * 100) or 1),
                                ft.Container(
                                    expand=max(100 - int(percent * 100), 0)) if percent < 1.0 else ft.Container(
                                    width=0),
                            ], spacing=0, expand=True),
                        ),
                    ], expand=True,
                ),
                ft.Container(height=6),
                ft.Row(controls=[
                    ft.Text(f"{int(percent * 100)}% виконано", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=11),
                    ft.Row(controls=[
                        ft.TextButton("Поповнити", style=ft.ButtonStyle(color=ft.Colors.ORANGE_400, padding=ft.Padding(left=0, right=8, top=0, bottom=0)), on_click=open_add_savings),
                        ft.TextButton("Редагувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), padding=ft.Padding(left=0, right=8, top=0, bottom=0)), on_click=open_edit),
                        ft.TextButton("Видалити", style=ft.ButtonStyle(color=ft.Colors.RED_400, padding=ft.Padding(left=0, right=0, top=0, bottom=0)), on_click=do_delete),
                    ], spacing=0),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ], spacing=0),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            border_radius=16,
            padding=18,
        )

    def done_card(g):
        def do_delete(e):
            show_confirm_dialog(page, "Видалити ціль?", f"Ціль «{g['title']}» буде видалена.", lambda: (delete_goal(g["id"]), refresh()), "Видалити", danger=True)

        return ft.Container(
            content=ft.Row(controls=[
                ft.Container(content=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN_400, size=18), bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.GREEN_400), border_radius=8, padding=8, width=36, height=36),
                ft.Column(controls=[
                    ft.Text(g["title"], color=ft.Colors.with_opacity(0.7, ft.Colors.WHITE), size=14, weight=ft.FontWeight.W_500),
                    ft.Text(f"{format_currency(g['target'])} • {g.get('deadline') or '—'}", color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE), size=12),
                ], spacing=2, expand=True),
                ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.with_opacity(0.4, ft.Colors.RED_300), icon_size=16, on_click=do_delete),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.07, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=14, right=4, top=12, bottom=12),
        )

    refresh()

    def open_add_goal(e):
        tf_title = ft.TextField(label="Назва цілі", border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
        tf_target = ft.TextField(label="Сума (₴)", keyboard_type=ft.KeyboardType.NUMBER, border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
        tf_desc = ft.TextField(label="Опис (необов'язково)", border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
        date_text = ft.Text("Дедлайн: не вказано", color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), size=13)
        chosen_deadline = {"value": ""}

        def on_date_change(ev):
            chosen_deadline["value"] = ev.control.value.strftime("%Y-%m-%d") if ev.control.value else ""
            date_text.value = f"Дедлайн: {chosen_deadline['value'] or 'не вказано'}"
            page.update()

        def open_dp(ev):
            page.show_dialog(ft.DatePicker(
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2035, 12, 31),
                value=datetime.now(),
                on_change=on_date_change,
            ))

        def do_add(ev):
            try:
                target = float(tf_target.value.replace(",", "."))
            except (ValueError, AttributeError):
                show_snack(page, "Введіть коректну суму", success=False)
                return
            ok, msg = add_goal(tf_title.value or "", target, tf_desc.value or "", chosen_deadline["value"])
            page.pop_dialog()
            show_snack(page, msg, success=ok)
            if ok:
                refresh()

        dlg = ft.AlertDialog(
            bgcolor="#1a1a1a",
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Text("Нова ціль", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                    ft.Container(height=16),
                    tf_title,
                    ft.Container(height=8),
                    tf_target,
                    ft.Container(height=8),
                    tf_desc,
                    ft.Container(height=8),
                    ft.Row(controls=[date_text, ft.IconButton(ft.Icons.CALENDAR_MONTH, icon_color=ft.Colors.ORANGE_400, icon_size=20, on_click=open_dp)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=16),
                    ft.Row(controls=[
                        ft.OutlinedButton("Скасувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: page.pop_dialog(), expand=True),
                        ft.Button("Додати", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0), on_click=do_add, expand=True),
                    ], spacing=12),
                ], tight=True, spacing=0),
                width=320, padding=20,
            ),
        )
        page.show_dialog(dlg)

    header_section = ft.Container(
        content=ft.Row(controls=[
            ft.Column(controls=[
                ft.Text("Фінансові цілі", color=ft.Colors.WHITE, size=22, weight=ft.FontWeight.W_700),
                ft.Text("Відстежуйте свій прогрес", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=13),
            ], spacing=3, expand=True),
            ft.Button("+ Ціль", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE,
                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                      height=38, on_click=open_add_goal),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding(left=20, right=20, top=20, bottom=12),
    )

    summary_row = ft.Container(
        content=ft.Row(controls=[
            ft.Column(controls=[summary_income, ft.Text("Накопичено", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3, expand=True),
            ft.Container(width=1, height=36, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            ft.Column(controls=[summary_remaining, ft.Text("Залишилось", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3, expand=True),
            ft.Container(width=1, height=36, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            ft.Column(controls=[summary_done, ft.Text("Виконано", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3, expand=True),
        ]),
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=14,
        padding=ft.Padding(left=16, right=16, top=16, bottom=16),
        margin=ft.Margin.symmetric(horizontal=20, vertical=4),
    )

    return ft.View(
        route="/goals",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(controls=[
                custom_appbar,
                ft.Column(controls=[
                    header_section,
                    summary_row,
                    ft.Container(content=goals_column, padding=ft.Padding(left=20, right=20, top=4, bottom=24)),
                ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0),
            ], spacing=0, expand=True),
        ],
    )
