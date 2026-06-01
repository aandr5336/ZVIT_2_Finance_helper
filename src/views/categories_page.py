import flet as ft
from src.models import *


def categories_view(page):

    state = {"filter": "Всі"}

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
        page.show_dialog(ft.SnackBar(ft.Text("Ви зараз на сторінці категорій.", color=ft.Colors.WHITE), bgcolor=ft.Colors.ORANGE_600))

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

    cats_column = ft.Column(spacing=10)
    stats_total = ft.Text("0", color=ft.Colors.WHITE, size=20, weight=ft.FontWeight.W_700)
    stats_tx = ft.Text("0", color=ft.Colors.ORANGE_300, size=20, weight=ft.FontWeight.W_700)
    stats_sum = ft.Text("₴0", color=ft.Colors.RED_400, size=20, weight=ft.FontWeight.W_700)
    filter_row_ref = ft.Ref[ft.Row]()

    def refresh(search=""):
        flt = state["filter"]
        cat_type = None
        if flt == "Витрати":
            cat_type = "expense"
        elif flt == "Дохід":
            cat_type = "income"

        cats = get_categories(cat_type=cat_type)
        if search:
            s = search.lower()
            cats = [c for c in cats if s in c["name"].lower()]

        stats_total.value = str(len(cats))
        stats_tx.value = str(sum(c["tx_count"] for c in cats))
        stats_sum.value = format_currency(sum(c["total"] for c in cats))

        cats_column.controls.clear()
        if not cats:
            cats_column.controls.append(
                ft.Container(
                    content=ft.Text("Категорій не знайдено", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=14, text_align=ft.TextAlign.CENTER),
                    padding=40, alignment=ft.Alignment.CENTER,
                )
            )
        else:
            grid = ft.ResponsiveRow(controls=[], spacing=10, run_spacing=10)
            for c in cats:
                cat_color = ft.Colors.ORANGE_400

                def make_edit(cat):
                    def do_edit(e):
                        tf_name = ft.TextField(label="Назва", value=cat["name"], border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
                        def do_save(ev):
                            ok, msg = update_category(cat["id"], tf_name.value or "", cat["icon"], cat["color"])
                            page.pop_dialog()
                            show_snack(page, msg, success=ok)
                            if ok:
                                refresh(search_field.value or "")
                        dlg = ft.AlertDialog(
                            bgcolor="#1a1a1a",
                            content=ft.Container(content=ft.Column(controls=[
                                ft.Text("Редагувати категорію", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                                ft.Container(height=16),
                                tf_name,
                                ft.Container(height=16),
                                ft.Row(controls=[
                                    ft.OutlinedButton("Скасувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: page.pop_dialog(), expand=True),
                                    ft.Button("Зберегти", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0), on_click=do_save, expand=True),
                                ], spacing=12),
                            ], tight=True, spacing=0), width=300, padding=20),
                        )
                        page.show_dialog(dlg)
                    return do_edit

                def make_delete(cat):
                    def do_delete(e):
                        show_confirm_dialog(page, "Видалити категорію?", f"Категорія «{cat['name']}» буде видалена.", lambda: (delete_category(cat["id"]), refresh(search_field.value or "")), "Видалити", danger=True)
                    return do_delete

                grid.controls.append(
                    ft.Column(col={"xs": 6}, controls=[
                        ft.Container(
                            content=ft.Column(controls=[
                                ft.Row(controls=[
                                    ft.Container(content=ft.Icon(ft.Icons.CATEGORY_OUTLINED, color=cat_color, size=20), bgcolor=ft.Colors.with_opacity(0.12, cat_color), border_radius=10, padding=10, width=42, height=42),
                                    ft.Container(expand=True),
                                    ft.Row(controls=[
                                        ft.IconButton(ft.Icons.EDIT_OUTLINED, icon_color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE), icon_size=16, on_click=make_edit(c)),
                                        ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.with_opacity(0.25, ft.Colors.RED_300), icon_size=16, on_click=make_delete(c)),
                                    ], spacing=0),
                                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                                ft.Container(height=4),
                                ft.Text(c["name"], color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_600),
                                ft.Text(format_currency(c["total"]), color=cat_color, size=16, weight=ft.FontWeight.W_700),
                                ft.Text(f"{c['tx_count']} транзакцій", color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE), size=11),
                                ft.Container(
                                    content=ft.Text("Витрата" if c["type"] == "expense" else "Дохід",
                                                    color=ft.Colors.RED_300 if c["type"] == "expense" else ft.Colors.GREEN_300, size=10),
                                    bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.RED_300 if c["type"] == "expense" else ft.Colors.GREEN_300),
                                    border_radius=4,
                                    padding=ft.Padding(left=6, right=6, top=2, bottom=2),
                                ),
                            ], spacing=2),
                            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                            border=ft.Border.all(1, ft.Colors.with_opacity(0.09, ft.Colors.WHITE)),
                            border_radius=14, padding=14,
                        )
                    ])
                )
            cats_column.controls.append(grid)
        page.update()

    refresh()

    search_field = ft.TextField(
        hint_text="Пошук категорій...",
        border_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        focused_border_color=ft.Colors.ORANGE_400,
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border_radius=10, height=44,
        text_style=ft.TextStyle(color=ft.Colors.WHITE, size=14),
        hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE)),
        prefix_icon=ft.Icons.SEARCH,
        content_padding=ft.Padding(left=0, right=12, top=0, bottom=0),
        on_change=lambda e: refresh(e.control.value),
    )

    def make_filter_btns(active):
        return [
            ft.Button(label, bgcolor=ft.Colors.ORANGE_700 if label == active else ft.Colors.with_opacity(0.0, ft.Colors.WHITE),
                      color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0),
                      height=34, on_click=lambda e, l=label: set_filter(l))
            for label in ["Всі", "Витрати", "Дохід"]
        ]

    def set_filter(label):
        state["filter"] = label
        filter_row_ref.current.controls = make_filter_btns(label)
        refresh(search_field.value or "")
        page.update()

    def open_add_category(e):
        tf_name = ft.TextField(label="Назва категорії", border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE), focused_border_color=ft.Colors.ORANGE_400, bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE), color=ft.Colors.WHITE, label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)), border_radius=10)
        dd_type = ft.Dropdown(
            label="Тип",
            value="expense",
            options=[ft.DropdownOption("expense", "Витрата"), ft.dropdown.Option("income", "Дохід")],
            border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            focused_border_color=ft.Colors.ORANGE_400,
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
        )
        def do_add(ev):
            ok, msg = add_category(tf_name.value or "", "category", "#FF9800", dd_type.value)
            page.pop_dialog()
            show_snack(page, msg, success=ok)
            if ok:
                refresh(search_field.value or "")
        dlg = ft.AlertDialog(
            bgcolor="#1a1a1a",
            content=ft.Container(content=ft.Column(controls=[
                ft.Text("Нова категорія", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                ft.Container(height=16),
                tf_name,
                ft.Container(height=8),
                dd_type,
                ft.Container(height=16),
                ft.Row(controls=[
                    ft.OutlinedButton("Скасувати", style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: page.pop_dialog(), expand=True),
                    ft.Button("Додати", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0), on_click=do_add, expand=True),
                ], spacing=12),
            ], tight=True, spacing=0), width=300, padding=20),
        )
        page.show_dialog(dlg)

    return ft.View(
        route="/categories",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(controls=[
                custom_appbar,
                ft.Column(controls=[
                    ft.Container(
                        content=ft.Row(controls=[
                            ft.Column(controls=[
                                ft.Text("Категорії", color=ft.Colors.WHITE, size=22, weight=ft.FontWeight.W_700),
                                ft.Text("Управління категоріями", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=13),
                            ], spacing=3, expand=True),
                            ft.Button("+ Категорія", bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                                      height=38, on_click=open_add_category),
                        ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.Padding(left=20, right=20, top=20, bottom=12),
                    ),
                    ft.Container(content=search_field, padding=ft.Padding(left=20, right=20, top=0, bottom=8)),
                    ft.Container(
                        content=ft.Row(ref=filter_row_ref, controls=make_filter_btns("Всі"), spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
                        border_radius=12, padding=6,
                        margin=ft.Margin.symmetric(horizontal=20, vertical=4),
                    ),
                    ft.Container(
                        content=ft.Row(controls=[
                            ft.Column(controls=[stats_total, ft.Text("Категорій", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3, expand=True),
                            ft.Container(width=1, height=36, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                            ft.Column(controls=[stats_tx, ft.Text("Транзакцій", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3, expand=True),
                            ft.Container(width=1, height=36, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
                            ft.Column(controls=[stats_sum, ft.Text("Всього витрат", color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=11)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=3, expand=True),
                        ]),
                        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
                        border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
                        border_radius=14,
                        padding=ft.Padding(left=16, right=16, top=16, bottom=16),
                        margin=ft.Margin.symmetric(horizontal=20, vertical=4),
                    ),
                    ft.Container(content=cats_column, padding=ft.Padding(left=20, right=20, top=8, bottom=24)),
                ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0),
            ], spacing=0, expand=True),
        ],
    )
