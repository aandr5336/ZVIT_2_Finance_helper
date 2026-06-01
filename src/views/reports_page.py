import flet as ft
from src.models import *


def reports_view(page):

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
        await page.push_route("/budget")

    async def go_goals(e):
        page.pop_dialog()
        await page.push_route("/goals")

    async def go_reports(e):
        page.pop_dialog()
        page.show_dialog(ft.SnackBar(ft.Text("Ви зараз на сторінці звітів.", color=ft.Colors.WHITE), bgcolor=ft.Colors.ORANGE_600))

    async def go_categories(e):
        page.pop_dialog()
        await page.push_route("/categories")

    async def go_settings(e):
        page.pop_dialog()
        await page.push_route("/settings")

    custom_appbar = ft.Container(
        content=ft.Row(controls=[
            ft.Row(controls=[
                ft.Icon(ft.Icons.SHOW_CHART, color=ft.Colors.ORANGE_300, size=20),
                ft.Text("Finance Helper", color=ft.Colors.WHITE, size=18, weight=ft.FontWeight.W_600),
            ], spacing=8, expand=True),
            ft.IconButton(ft.Icons.SETTINGS_OUTLINED, icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE), icon_size=20, on_click=lambda e: open_settings_dialog(page)),
            ft.IconButton(ft.Icons.MENU, icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE), icon_size=20,
                          on_click=lambda e: open_left_menu_dialog(page, go_home, go_control_panel, go_transactions, go_budget, go_goals, go_reports, go_categories, go_settings)),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        gradient=gradient_for_appbar, height=60,
        padding=ft.Padding(left=20, right=8, top=0, bottom=0),
        border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE))),
    )

    month_label = ft.Text("", color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_600, expand=True, text_align=ft.TextAlign.CENTER)
    net_income_text = ft.Text("₴ 0", color=ft.Colors.GREEN_400, size=28, weight=ft.FontWeight.W_700)
    income_text = ft.Text("₴ 0", color=ft.Colors.GREEN_400, size=16, weight=ft.FontWeight.W_600)
    expenses_text = ft.Text("₴ 0", color=ft.Colors.RED_400, size=16, weight=ft.FontWeight.W_600)
    savings_rate_text = ft.Text("0%", color=ft.Colors.ORANGE_300, size=16, weight=ft.FontWeight.W_600)
    categories_column = ft.Column(spacing=14)
    compare_column = ft.Column(spacing=12)
    bar_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, vertical_alignment=ft.CrossAxisAlignment.END)

    def refresh():
        m = state["month"]
        month_label.value = format_month_label(m)
        report = get_monthly_report(m)
        prev = prev_month(m)
        comp = compare_months(m, prev)

        net_income_text.value = format_currency(report["balance"])
        income_text.value = format_currency(report["income"])
        expenses_text.value = format_currency(report["expenses"])
        savings_rate_text.value = f"{get_savings_rate(m)}%"


        history = get_last_n_months_summary(5)
        bar_row.controls.clear()
        if history:
            max_val = max(max(h["income"], h["expenses"]) for h in history) or 1
            for h in history:
                ih = int(120 * h["income"] / max_val)
                eh = int(120 * h["expenses"] / max_val)
                lbl = h["month"][5:]
                bar_row.controls.append(
                    ft.Column(controls=[
                        ft.Row(controls=[
                            ft.Container(bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREEN_400), border_radius=ft.BorderRadius.only(top_left=4, top_right=4), width=14, height=max(ih, 2)),
                            ft.Container(bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.RED_400), border_radius=ft.BorderRadius.only(top_left=4, top_right=4), width=14, height=max(eh, 2)),
                        ], spacing=3, vertical_alignment=ft.CrossAxisAlignment.END),
                        ft.Text(lbl, color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11, text_align=ft.TextAlign.CENTER),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6)
                )


        categories_column.controls.clear()
        for cat in report["by_category"]:
            pct = int(cat.get("percent", 0))
            categories_column.controls.append(
                ft.Column(controls=[
                    ft.Row(controls=[
                        ft.Text(cat["name"], color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE), size=13, expand=True),
                        ft.Text(format_currency(cat["total"]), color=ft.Colors.WHITE, size=13, weight=ft.FontWeight.W_600),
                        ft.Text(f"{cat.get('percent', 0)}%", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=12),
                    ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    ft.Row(
                        controls=[
                            ft.Container(
                                bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE),
                                border_radius=3, height=4, expand=True,
                                content=ft.Row(controls=[
                                    ft.Container(bgcolor=ft.Colors.ORANGE_400, border_radius=3, height=4,
                                                 expand=pct or 1),
                                    ft.Container(expand=max(100 - pct, 0)) if pct < 100 else ft.Container(width=0),
                                ], spacing=0, expand=True),
                            ),
                        ], expand=True,
                    ),
                ], spacing=6)
            )

        if not report["by_category"]:
            categories_column.controls.append(ft.Text("Немає даних за цей місяць", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=13))


        compare_column.controls.clear()
        compare_column.controls.append(
            ft.Container(height=1, bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.WHITE))
        )

        def cmp_row(label, diff, pct):
            is_up = diff > 0
            color = ft.Colors.RED_400 if is_up else ft.Colors.GREEN_400
            arrow = ft.Icons.ARROW_UPWARD if is_up else ft.Icons.ARROW_DOWNWARD
            return ft.Row(controls=[
                ft.Text(label, color=ft.Colors.with_opacity(0.65, ft.Colors.WHITE), size=13, expand=True),
                ft.Text(format_currency(comp["a"].get(label.lower(), 0)), color=ft.Colors.WHITE, size=13, weight=ft.FontWeight.W_500),
                ft.Row(controls=[
                    ft.Icon(arrow, color=color, size=13),
                    ft.Text(format_currency(abs(diff)), color=color, size=12),
                ], spacing=2),
            ], spacing=10)

        compare_column.controls.append(ft.Container(height=10))
        compare_column.controls.append(cmp_row("Дохід", comp["income_diff"], comp["income_pct"]))
        compare_column.controls.append(cmp_row("Витрати", comp["expenses_diff"], comp["expenses_pct"]))
        compare_column.controls.append(cmp_row("Баланс", comp["balance_diff"], None))

        page.update()

    refresh()

    def prev_m(e):
        state["month"] = prev_month(state["month"])
        refresh()

    def next_m(e):
        state["month"] = next_month(state["month"])
        refresh()

    month_switcher = ft.Container(
        content=ft.Row(controls=[
            ft.IconButton(ft.Icons.CHEVRON_LEFT, icon_color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), icon_size=20, on_click=prev_m),
            month_label,
            ft.IconButton(ft.Icons.CHEVRON_RIGHT, icon_color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), icon_size=20, on_click=next_m),
        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=10,
        margin=ft.Margin.symmetric(horizontal=20, vertical=8),
        padding=ft.Padding(left=4, right=4, top=4, bottom=4),
    )

    month_card = ft.Container(
        content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Column(controls=[
                    ft.Text("Чистий дохід", color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_500),
                    net_income_text,
                ], spacing=3, expand=True),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(height=16),
            ft.Row(controls=[
                ft.Column(controls=[ft.Text("Дохід", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=12), income_text], spacing=3, expand=True),
                ft.Container(width=1, height=32, bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
                ft.Column(controls=[ft.Text("Витрати", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=12), expenses_text], spacing=3, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(width=1, height=32, bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.WHITE)),
                ft.Column(controls=[ft.Text("Заощадження", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=12), savings_rate_text], spacing=3, expand=True, horizontal_alignment=ft.CrossAxisAlignment.END),
            ]),
        ], spacing=0),
        gradient=ft.LinearGradient(begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1), colors=[ft.Colors.with_opacity(0.18, ft.Colors.ORANGE_700), ft.Colors.with_opacity(0.08, ft.Colors.WHITE)]),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.ORANGE_400)),
        border_radius=16, padding=20,
        margin=ft.Margin.symmetric(horizontal=20, vertical=8),
    )

    bar_section = ft.Container(
        content=ft.Column(controls=[
            ft.Row(controls=[
                ft.Text("Дохід vs Витрати", color=ft.Colors.WHITE, size=15, weight=ft.FontWeight.W_700),
                ft.Row(controls=[
                    ft.Row(controls=[ft.Container(width=10, height=10, bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREEN_400), border_radius=2), ft.Text("Дохід", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=11)], spacing=4),
                    ft.Row(controls=[ft.Container(width=10, height=10, bgcolor=ft.Colors.with_opacity(0.7, ft.Colors.RED_400), border_radius=2), ft.Text("Витрати", color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=11)], spacing=4),
                ], spacing=12),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=12),
            bar_row,
        ], spacing=0),
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=14, padding=18,
    )

    cats_section = ft.Container(
        content=ft.Column(controls=[
            ft.Text("Топ категорій витрат", color=ft.Colors.WHITE, size=15, weight=ft.FontWeight.W_700),
            ft.Container(height=8),
            categories_column,
        ], spacing=0),
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=14, padding=18,
    )

    compare_section = ft.Container(
        content=ft.Column(controls=[
            ft.Text("Порівняння з попереднім місяцем", color=ft.Colors.WHITE, size=15, weight=ft.FontWeight.W_700),
            compare_column,
        ], spacing=0),
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
        border_radius=14, padding=18,
    )

    return ft.View(
        route="/reports",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(controls=[
                custom_appbar,
                ft.Column(controls=[
                    ft.Container(
                        content=ft.Row(controls=[
                            ft.Column(controls=[
                                ft.Text("Звіти", color=ft.Colors.WHITE, size=22, weight=ft.FontWeight.W_700),
                                ft.Text("Аналітика та статистика", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=13),
                            ], spacing=3, expand=True),
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.Padding(left=20, right=20, top=20, bottom=12),
                    ),
                    month_switcher,
                    month_card,
                    ft.Container(
                        content=ft.Column(controls=[bar_section, ft.Container(height=4), cats_section, ft.Container(height=4), compare_section], spacing=12),
                        padding=ft.Padding(left=20, right=20, top=4, bottom=24),
                    ),
                ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0),
            ], spacing=0, expand=True),
        ],
    )
