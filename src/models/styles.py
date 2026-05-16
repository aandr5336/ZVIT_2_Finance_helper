import flet as ft


style_for_tf_text_reg_page = ft.TextStyle(
    size=15,
    weight= ft.FontWeight.W_800,
    color=ft.Colors.WHITE,
)


style_for_text_btn_reg_page = ft.ButtonStyle(
    color=ft.Colors.WHITE,
    text_style = style_for_tf_text_reg_page,
)


style_for_tf_label_reg_page = ft.TextStyle(
    size=15,
    weight= ft.FontWeight.W_100,
    color=ft.Colors.WHITE,
)




style_for_default_btn = ft.ButtonStyle(
    color = ft.Colors.WHITE,
    bgcolor = ft.Colors.ORANGE_900,
    overlay_color = ft.Colors.RED_700,
    # shadow_color,
    # elevation,
    # animation_duration,
    # padding,
    # side,
    shape=ft.BeveledRectangleBorder(radius=15),
    # alignment,
    # enable_feedback,
    # text_style,
    # icon_size,
    # icon_color,
    # visual_density,
    # mouse_cursor,
)