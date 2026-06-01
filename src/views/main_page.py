import flet as ft
from src.models import *
from src.assets import *


def home_view(page):

    async def open_login(e):
        await page.push_route("/login")

    async def go_home(e):
        page.pop_dialog()
        page.show_dialog(
            ft.SnackBar(
                ft.Text("Ви зараз на головній сторінці.", color = ft.Colors.WHITE),
                bgcolor = ft.Colors.ORANGE_600,
            )
        )

    async def go_control_panel(e):
        await page.push_route("/control_panel")

    async def go_transactions(e):
        await page.push_route("/transactions")

    async def go_budget(e):
        await page.push_route("/budget")

    async def go_goals(e):
        await page.push_route("/goals")

    async def go_reports(e):
        await page.push_route("/reports")

    async def go_categories(e):
        await page.push_route("/categories")

    async def go_settings(e):
        await page.push_route("/settings")


    hero = ft.Container(
        content=ft.Text(
            "Особисті фінанси нового покоління",
            color=ft.Colors.ORANGE_300,
            size=13,
            weight=ft.FontWeight.W_500,
            style = ft.TextStyle(letter_spacing=1.2)
        ),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.ORANGE_300)),
        border_radius=20,
        padding=ft.Padding(left=14, right=14, top=6, bottom=6),
        margin=ft.Margin.only(bottom=28),
    )

    hero_title = ft.Text(
        "Контролюй свої\nфінанси розумно",
        size=52,
        weight=ft.FontWeight.W_700,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
    )

    hero_subtitle = ft.Text(
        "Finance Helper — ваш помічник у контролі витрат і плануванні бюджету.",
        size=17,
        color=ft.Colors.with_opacity(0.65, ft.Colors.WHITE),
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.W_400,
    )

    btn_login = ft.Button(
        content=ft.Text(
            "Увійти до акаунту",
            color=ft.Colors.WHITE,
            size=16,
            weight=ft.FontWeight.W_500,
        ),
        on_click=open_login,
        bgcolor=ft.Colors.ORANGE_700,
        style = ft.ButtonStyle(padding=ft.Padding(left=40, right=40, top=20, bottom=20)),
    )

    cards_row = (ft.Column(
        controls=[
            card_maker(ft.Icons.ANALYTICS_OUTLINED, "Аналітика", "Детальні графіки та звіти по витратах"),
            card_maker(ft.Icons.SAVINGS_OUTLINED, "Накопичення", "Відстежуй цілі та прогрес заощаджень"),
            card_maker(ft.Icons.NOTIFICATIONS_OUTLINED, "Сповіщення", "Нагадування про рахунки та ліміти"),
        ],
        spacing=16,
        alignment=ft.MainAxisAlignment.CENTER, ))  if page.width <1000 else (ft.Row(
        controls=[
            card_maker(ft.Icons.ANALYTICS_OUTLINED, "Аналітика", "Детальні графіки та звіти по витратах"),
            card_maker(ft.Icons.SAVINGS_OUTLINED, "Накопичення", "Відстежуй цілі та прогрес заощаджень"),
            card_maker(ft.Icons.NOTIFICATIONS_OUTLINED, "Сповіщення", "Нагадування про рахунки та ліміти"),
        ],
        spacing=16,
        alignment=ft.MainAxisAlignment.CENTER, ))


    hero_section = ft.Stack(
        controls=[
            ft.Container(
                image=ft.DecorationImage(
                    src="bg_image_for_main_page.png",
                    fit=ft.BoxFit.COVER,
                ),
                expand=True,
                height=620,
            ),
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, -1),
                    end=ft.Alignment(0, 1),
                    colors=[
                        ft.Colors.with_opacity(0.75, ft.Colors.BLACK),
                        ft.Colors.with_opacity(0.92, ft.Colors.BLACK),
                    ],
                ),
                expand=True,
                height=620,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        hero,
                        hero_title,
                        ft.Container(height=16),
                        hero_subtitle,
                        ft.Container(height=36),
                        btn_login,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                expand=True,
                height=620,
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding(left=40, right=40, top=0, bottom=0),
            ),
        ],
    )


    card_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Чому Finance Helper?",
                    color=ft.Colors.WHITE,
                    size=26,
                    weight=ft.FontWeight.W_700,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=8),
                ft.Text(
                    "Все необхідне для фінансового контролю в одному місці",
                    color=ft.Colors.with_opacity(0.55, ft.Colors.WHITE),
                    size=15,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=32),
                cards_row,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(left=32, right=32, top=48, bottom=48),
        bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
    )


    custom_appbar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SHOW_CHART, color=ft.Colors.ORANGE_300, size=22),
                        ft.Text(
                            "Finance Helper",
                            color=ft.Colors.WHITE,
                            size=18,
                            weight=ft.FontWeight.W_600,
                            style = ft.TextStyle(letter_spacing=0.3,)
                        ),
                    ],
                    spacing=8,
                    expand=True,
                ),
                ft.IconButton(
                    ft.Icons.SETTINGS_OUTLINED,
                    icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                    icon_size=20,
                    on_click=lambda e: open_settings_dialog(page),
                    tooltip="Налаштування",
                ),
                ft.IconButton(
                    ft.Icons.MENU,
                    icon_color=ft.Colors.with_opacity(0.8, ft.Colors.WHITE),
                    icon_size=20,
                    on_click=lambda e: open_left_menu_dialog(page, go_home, go_control_panel, go_transactions, go_budget, go_goals, go_reports, go_categories, go_settings),
                    tooltip="Меню",
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        gradient=gradient_for_appbar,
        height=60,
        padding=ft.Padding(left=20, right=8, top=0, bottom=0),
        border=ft.Border(
            bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE))
        ),
    )

    return ft.View(
        route="/",
        padding=0,
        bgcolor=ft.Colors.with_opacity(1, ft.Colors.BLACK),
        controls=[ft.Column(
                controls=[
                    custom_appbar,
                    ft.Column(
                        controls=[
                            hero_section,
                            card_section,
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                        spacing=0,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
        ],
    )