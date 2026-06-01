import flet as ft
import datetime
from src.models import *


def transactions_view(page):

    selected_filter = {"value": "Всі"}
    selected_date = {"value": None}

    async def go_home(e):
        await page.push_route("/")

    async def go_control_panel(e):
        page.pop_dialog()
        await page.push_route("/control_panel")

    async def go_transactions(e):
        page.pop_dialog()
        page.show_dialog(ft.SnackBar(ft.Text("Ви зараз на сторінці транзакцій.", color=ft.Colors.WHITE), bgcolor=ft.Colors.ORANGE_600))

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
        await page.push_route("/settings")

    month = current_month()
    summary = get_monthly_summary(month)


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


    transactions_column = ft.Column(spacing=20)

    def refresh_list(search_text="", tx_filter=None):
        flt = None
        if tx_filter == "Дохід":
            flt = "income"
        elif tx_filter == "Витрати":
            flt = "expense"

        txs = get_transactions(tx_type=flt, month=month, search=search_text)


        groups = {}
        for t in txs:
            day = t["created_at"][:10]
            if day not in groups:
                groups[day] = []
            groups[day].append(t)

        transactions_column.controls.clear()
        if not groups:
            transactions_column.controls.append(
                ft.Container(
                    content=ft.Text("Транзакцій не знайдено", color=ft.Colors.with_opacity(0.4, ft.Colors.WHITE), size=14, text_align=ft.TextAlign.CENTER),
                    padding=40,
                    alignment=ft.Alignment.CENTER,
                )
            )
        else:
            for day, items in groups.items():
                day_items = []
                for t in items:
                    is_expense = t["type"] == "expense"
                    color = ft.Colors.RED_400 if is_expense else ft.Colors.GREEN_400
                    sign = "-" if is_expense else "+"
                    time_str = t["created_at"][11:16]

                    def make_delete(tx_id):
                        def do_delete(e):
                            delete_transaction(tx_id)
                            refresh_list(search_field.value or "", selected_filter["value"])
                            page.update()
                        return do_delete

                    day_items.append(
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Icon(ft.Icons.RECEIPT_OUTLINED, color=ft.Colors.ORANGE_400, size=18),
                                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_400),
                                        border_radius=10, padding=10, width=42, height=42,
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(t.get("note") or t.get("category", "—"), color=ft.Colors.WHITE, size=14, weight=ft.FontWeight.W_500),
                                            ft.Row(
                                                controls=[
                                                    ft.Container(
                                                        content=ft.Text(t.get("category", ""), color=ft.Colors.ORANGE_300, size=11),
                                                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_300),
                                                        border_radius=4,
                                                        padding=ft.Padding(left=6, right=6, top=2, bottom=2),
                                                    ),
                                                    ft.Text(time_str, color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE), size=11),
                                                ],
                                                spacing=6,
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True,
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(f"{sign}₴{t['amount']:,.0f}", color=color, size=15, weight=ft.FontWeight.W_600),
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                        spacing=2,
                                    ),
                                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=ft.Colors.with_opacity(0.4, ft.Colors.RED_300), icon_size=16, on_click=make_delete(t["id"])),
                                ],
                                spacing=12,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
                            border=ft.Border.all(1, ft.Colors.with_opacity(0.07, ft.Colors.WHITE)),
                            border_radius=12,
                            padding=ft.Padding(left=14, right=4, top=12, bottom=12),
                        )
                    )

                transactions_column.controls.append(
                    ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text(day, color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=12, weight=ft.FontWeight.W_600),
                                padding=ft.Padding(left=4, right=0, top=0, bottom=0),
                            ),
                            *day_items,
                        ],
                        spacing=6,
                    )
                )
        page.update()

    refresh_list()


    search_field = ft.TextField(
        hint_text="Пошук транзакцій...",
        border_color=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
        focused_border_color=ft.Colors.ORANGE_400,
        bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
        border_radius=10, height=44,
        text_style=ft.TextStyle(color=ft.Colors.WHITE, size=14),
        hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.35, ft.Colors.WHITE)),
        prefix_icon=ft.Icons.SEARCH,
        content_padding=ft.Padding(left=0, right=12, top=0, bottom=0),
        on_change=lambda e: refresh_list(e.control.value, selected_filter["value"]),
    )


    filter_row = ft.Ref[ft.Row]()

    def make_filter_buttons(active):
        return [
            ft.Button(
                label,
                bgcolor=ft.Colors.ORANGE_700 if label == active else ft.Colors.with_opacity(0.07, ft.Colors.WHITE),
                color=ft.Colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0),
                height=34,
                on_click=lambda e, l=label: set_filter(l),
            )
            for label in ["Всі", "Дохід", "Витрати"]
        ]

    def set_filter(label):
        selected_filter["value"] = label
        filter_row.current.controls = make_filter_buttons(label)
        refresh_list(search_field.value or "", label)
        page.update()


    def open_add_dialog(e):
        cats = get_categories()
        if not cats:
            show_snack(page, "Немає категорій. Спочатку додайте категорію.", success=False)
            return



        expense_cats = [c for c in cats if c["type"] == "expense"]
        income_cats = [c for c in cats if c["type"] == "income"]
        cat_options_expense = [ft.dropdown.Option(str(c["id"]), c["name"],) for c in expense_cats]
        cat_options_income = [ft.dropdown.Option(str(c["id"]), c["name"]) for c in income_cats]

        dd_category = ft.Dropdown(
            label="Категорія",
            options=cat_options_expense,
            value=str(expense_cats[0]["id"]) if expense_cats else None,
            border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            focused_border_color=ft.Colors.ORANGE_400,
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
            color=ft.Colors.WHITE,
            menu_height = 300,
            label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
        )

        def on_type_change(e):
            if dd_type.value == "expense":
                dd_category.options = cat_options_expense
                dd_category.value = str(expense_cats[0]["id"]) if expense_cats else None
            else:
                dd_category.options = cat_options_income
                dd_category.value = str(income_cats[0]["id"]) if income_cats else None
            page.update()

        dd_type = ft.Dropdown(
            label="Тип",
            value="expense",
            options=[ft.dropdown.Option("expense", "Витрата"), ft.dropdown.Option("income", "Дохід")],
            border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            focused_border_color=ft.Colors.ORANGE_400,
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
            on_text_change=on_type_change,
        )

        tf_amount = ft.TextField(
            label="Сума (₴)",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            focused_border_color=ft.Colors.ORANGE_400,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
            border_radius=10,
        )

        tf_note = ft.TextField(
            label="Примітка (необов'язково)",
            border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
            focused_border_color=ft.Colors.ORANGE_400,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
            border_radius=10,
        )

        date_text = ft.Text(
            "Дата: сьогодні",
            color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE),
            size=13,
        )
        chosen_date = {"value": None}

        def on_date_change(e):
            chosen_date["value"] = e.control.value.strftime("%Y-%m-%d") if e.control.value else None
            date_text.value = f"Дата: {chosen_date['value'] or 'сьогодні'}"
            page.update()

        def open_datepicker(e):
            page.show_dialog(ft.DatePicker(
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2030, 12, 31),
                value=datetime.now(),
                on_change=on_date_change,
            ))

        def do_add(e):
            try:
                amount = float(tf_amount.value.replace(",", "."))
            except (ValueError, AttributeError):
                show_snack(page, "Введіть коректну суму", success=False)
                return

            if not dd_category.value:
                show_snack(page, "Оберіть категорію", success=False)
                return

            ok, msg = add_transaction(
                category_id=int(dd_category.value),
                amount=amount,
                tx_type=dd_type.value,
                note=tf_note.value or "",
                date=chosen_date["value"] or "",
            )
            page.pop_dialog()
            show_snack(page, msg, success=ok)
            if ok:
                refresh_list(search_field.value or "", selected_filter["value"])

        dlg = ft.AlertDialog(
            bgcolor="#1a1a1a",
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Нова транзакція", color=ft.Colors.WHITE, size=17, weight=ft.FontWeight.W_700),
                        ft.Container(height=16),
                        dd_type,
                        ft.Container(height=8),
                        dd_category,
                        ft.Container(height=8),
                        tf_amount,
                        ft.Container(height=8),
                        tf_note,
                        ft.Container(height=8),
                        ft.Row(
                            controls=[
                                date_text,
                                ft.IconButton(ft.Icons.CALENDAR_MONTH, icon_color=ft.Colors.ORANGE_400, icon_size=20, on_click=open_datepicker),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=16),
                        ft.Row(
                            controls=[
                                ft.OutlinedButton(
                                    "Скасувати",
                                    style=ft.ButtonStyle(color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE), side=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)), shape=ft.RoundedRectangleBorder(radius=8)),
                                    on_click=lambda e: page.pop_dialog(),
                                    expand=True,
                                ),
                                ft.Button(
                                    "Додати",
                                    bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), elevation=0),
                                    on_click=do_add,
                                    expand=True,
                                ),
                            ],
                            spacing=12,
                        ),
                    ],
                    tight=True,
                    spacing=0,
                ),
                width=320,
                padding=20,
            ),
        )
        page.show_dialog(dlg)


    def summary_card(label, amount, color, icon):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(icon, color=color, size=18),
                    ft.Text(format_currency(amount), color=ft.Colors.WHITE, size=16, weight=ft.FontWeight.W_700),
                    ft.Text(label, color=ft.Colors.with_opacity(0.5, ft.Colors.WHITE), size=11),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.08, ft.Colors.WHITE)),
            border_radius=12,
            padding=ft.Padding(left=12, right=12, top=14, bottom=14),
            expand=True,
        )

    summary_row = ft.Container(
        content=ft.Row(
            controls=[
                summary_card("Дохід", summary["income"], ft.Colors.GREEN_400, ft.Icons.ARROW_UPWARD),
                summary_card("Витрати", summary["expenses"], ft.Colors.RED_400, ft.Icons.ARROW_DOWNWARD),
                summary_card("Різниця", summary["balance"], ft.Colors.ORANGE_300, ft.Icons.BALANCE_OUTLINED),
            ],
            spacing=10,
        ),
        padding=ft.Padding(left=20, right=20, top=0, bottom=12),
    )

    header_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Транзакції", color=ft.Colors.WHITE, size=22, weight=ft.FontWeight.W_700),
                                ft.Text(format_month_label(month), color=ft.Colors.with_opacity(0.45, ft.Colors.WHITE), size=13),
                            ],
                            spacing=3,
                            expand=True,
                        ),
                        ft.Button(
                            "+ Додати",
                            bgcolor=ft.Colors.ORANGE_700, color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), elevation=0),
                            height=38,
                            on_click=open_add_dialog,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=4),
                search_field,
                ft.Container(height=4),
                ft.Row(ref=filter_row, controls=make_filter_buttons("Всі"), spacing=8, scroll=ft.ScrollMode.AUTO),
            ],
            spacing=8,
        ),
        padding=ft.Padding(left=20, right=20, top=20, bottom=12),
    )

    return ft.View(
        route="/transactions",
        padding=0,
        bgcolor=ft.Colors.BLACK,
        controls=[
            ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            header_section,
                            summary_row,
                            ft.Container(content=transactions_column, padding=ft.Padding(left=20, right=20, top=4, bottom=24)),
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
