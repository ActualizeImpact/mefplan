"""Common templates used between pages in the app."""
from __future__ import annotations

from .. import styles
from ..components.sidebar import sidebar
from ..components.navbar import navbar
from typing import Callable

import reflex as rx

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]

def menu_item_link(text, href):
    return rx.menu.item(
        rx.link(
            text,
            href=href,
            width="100%",
            color="inherit",
        ),
        _hover={
            "color": styles.accent_color,
            "background_color": styles.accent_text_color,
        },
    )

class ThemeState(rx.State):
    """The state for the theme of the app."""

    accent_color: str = "grass"
    gray_color: str = "gray"
    radius: str = "large"
    scaling: str = "100%"

def template(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventHandler | list[rx.event.EventHandler] | None = None,
    include_sidebar: bool = True,
    include_navbar: bool = True,
    hidden_routes: list[str] = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app."""

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        """The template for each page of the app."""
        # Get the meta tags for the page.
        all_meta = [*default_meta, *(meta or [])]

        def templated_page():
            content = rx.box(
                page_content(),
                **styles.main_content_style,
            )

            layout = rx.flex(
                rx.cond(
                    include_navbar,
                    navbar(hidden_routes=hidden_routes),
                    rx.box(),
                ),
                rx.cond(
                    include_sidebar,
                    sidebar(hidden_routes=hidden_routes),
                    rx.box(),
                ),
                content,
                **styles.template_page_style,
            )

            return layout

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def theme_wrap():
            return rx.theme(
                templated_page(),
                has_background=True,
                accent_color=ThemeState.accent_color,
                gray_color=ThemeState.gray_color,
                radius=ThemeState.radius,
                scaling=ThemeState.scaling,
            )

        return theme_wrap

    return decorator