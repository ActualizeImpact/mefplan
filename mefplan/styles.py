"""Styles for the app."""

import reflex as rx

border_radius = "var(--radius-2)"
border = f"1px solid {rx.color('gray', 5)}"
text_color = rx.color("gray", 11)
gray_color = rx.color("gray", 11)
gray_bg_color = rx.color("gray", 3)
accent_text_color = rx.color("accent", 10)
accent_color = rx.color("accent", 1)
accent_bg_color = rx.color("accent", 3)
hover_accent_color = {"_hover": {"color": accent_text_color}}
hover_accent_bg = {"_hover": {"background_color": accent_color}}
content_width_vw = "90vw"
sidebar_width = "300px"
sidebar_content_width = "16em"
max_width = "1920px"
color_box_size = ["2.25rem", "2.25rem", "2.5rem"]

template_page_style = {
    "padding_top": ["1em", "1em", "0em"],
    "padding_x": ["1em", "2em", "3em", "4em", "5em", "6em"],
    "width": "100%",
    "max_width": max_width,
    "margin": "auto",
    "display": "flex",
    "flex_direction": ["column", "column", "column", "column", "column", "row"],
    "height": "100vh",  # Add this to ensure the template takes up full viewport height
    "overflow": "hidden",  # Add this to prevent scrolling on the outer container
}

main_content_style = {
    "flex": "1",
    "width": "100%",
    "padding": "1em",
    "margin_bottom": "2em",
    "min_height": "100vh",  # Change this to ensure main content is at least full viewport height
    "overflow_y": "auto",  # Add this to enable scrolling in the main content area
}

sidebar_style = {
    "width": sidebar_width,
    "max_width": sidebar_width,
    "height": "100vh",
    "position": "sticky",
    "top": "0px",
    "left": "0px",
    "padding_x": "1em",
    "background_color": gray_bg_color,
    "display": ["none", "none", "none", "none", "none", "flex"],
    "overflow_y": "auto",  # Add this to enable scrolling within the sidebar if content overflows
}

navbar_style = {
    "display": ["flex", "flex", "flex", "flex", "flex", "none"],
    "position": "sticky",
    "background_color": rx.color("gray", 1),
    "top": "0px",
    "z_index": "5",
    "border_bottom": border,
    "width": "100%",
}

navbar_content_style = {
    "align_items": "center",
    "width": "100%",
    "padding_y": "1.25em",
    "padding_x": ["1em", "1em", "2em"],
    "max_width": max_width,
    "margin": "0 auto",
}

link_style = {
    "color": accent_text_color,
    "text_decoration": "none",
    **hover_accent_color,
}

overlapping_button_style = {
    "background_color": "white",
    "border_radius": border_radius,
}

markdown_style = {
    "code": lambda text: rx.code(text, color_scheme="gray"),
    "codeblock": lambda text, **props: rx.code_block(text, **props, margin_y="1em"),
    "a": lambda text, **props: rx.link(
        text,
        **props,
        font_weight="bold",
        text_decoration="underline",
        text_decoration_color=accent_text_color,
    ),
}

notification_badge_style = {
    "width": "1.25rem",
    "height": "1.25rem",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "position": "absolute",
    "right": "-0.35rem",
    "top": "-0.35rem",
}

ghost_input_style = {
    "--text-field-selection-color": "",
    "--text-field-focus-color": "transparent",
    "--text-field-border-width": "1px",
    "background-clip": "content-box",
    "background-color": "transparent",
    "box-shadow": "inset 0 0 0 var(--text-field-border-width) transparent",
    "color": "",
}

box_shadow_style = "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)"

color_picker_style = {
    "border_radius": "max(var(--radius-3), var(--radius-full))",
    "box_shadow": box_shadow_style,
    "cursor": "pointer",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "transition": "transform 0.15s ease-in-out",
    "_active": {
        "transform": "translateY(2px) scale(0.95)",
    },
}

base_stylesheets = [
    "https://use.typekit.net/clz6xwh.css",
]

base_style = {
    "font_family": "proxima-nova, sans-serif",
}
