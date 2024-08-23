"""Sidebar component for the app."""

from .. import styles

import reflex as rx


def sidebar_header() -> rx.Component:
    return rx.hstack(
        rx.color_mode_cond(
            rx.image(src="/CEP_W.png", height="5em"),
            rx.image(src="/CEP_W.png", height="5em"),
        ),
        rx.spacer(),
        align="center",
        width="100%",
        padding="0.35em",
        margin_bottom="1em",
    )


def sidebar_footer() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.text("Docs", size="3"),
            href="https://reflex.dev/docs/getting-started/introduction/",
            color_scheme="gray",
            underline="none",
        ),
        rx.link(
            rx.text("Site", size="3"),
            href="https://cepartners.io",
            color_scheme="gray",
            underline="none",
        ),
        rx.spacer(),
        rx.color_mode.button(style={"opacity": "0.8", "scale": "0.95"}),
        justify="start",
        align="center",
        width="100%",
        padding="0.35em",
    )


def sidebar_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=18)


def sidebar_item(text: str, url: str, icon: str = None) -> rx.Component:
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & (text == "Dashboard")
    )

    return rx.link(
        rx.hstack(
            (
                sidebar_item_icon(icon)
                if icon
                else rx.match(
                    text,
                    ("Dashboard", sidebar_item_icon("gauge")),
                    ("Tasks", sidebar_item_icon("clipboard-list")),
                    ("Workstreams", sidebar_item_icon("git-branch")),
                    ("Milestones", sidebar_item_icon("flag")),
                    ("Check-ins", sidebar_item_icon("check-circle")),
                    ("Meetings", sidebar_item_icon("users")),
                    ("Black Business Finder", sidebar_item_icon("search")),
                )
            ),
            rx.text(text, size="3", weight="regular"),
            color=rx.cond(
                active,
                styles.accent_text_color,
                styles.text_color,
            ),
            style={
                "_hover": {
                    "background_color": rx.cond(
                        active,
                        styles.accent_bg_color,
                        styles.gray_bg_color,
                    ),
                    "color": rx.cond(
                        active,
                        styles.accent_text_color,
                        styles.text_color,
                    ),
                    "opacity": "1",
                },
                "opacity": rx.cond(
                    active,
                    "1",
                    "0.95",
                ),
            },
            align="center",
            border_radius=styles.border_radius,
            width="100%",
            spacing="2",
            padding="0.35em",
        ),
        underline="none",
        href=url,
        width="100%",
    )


def sidebar(hidden_routes: list[str] = None) -> rx.Component:
    from reflex.page import get_decorated_pages

    ordered_page_routes = [
        "/",
        "/dashboard",
        "/tasks",
        "/workstreams",
        "/milestones",
        "/check-ins",
        "/meetings",
        "/blackbiz",
    ]

    pages = get_decorated_pages()

    ordered_pages = sorted(
        pages,
        key=lambda page: (
            ordered_page_routes.index(page["route"])
            if page["route"] in ordered_page_routes
            else len(ordered_page_routes)
        ),
    )

    # Filter out hidden routes
    visible_pages = [
        page for page in ordered_pages if page["route"] not in (hidden_routes or [])
    ]

    return rx.box(
        rx.vstack(
            sidebar_header(),
            rx.vstack(
                *[
                    sidebar_item(
                        text=page.get("title", page["route"].strip("/").capitalize()),
                        url=page["route"],
                    )
                    for page in visible_pages
                ],
                spacing="1",
                width="100%",
                overflow_y="auto",
                flex="1",
            ),
            rx.spacer(),
            rx.vstack(
                rx.vstack(
                    sidebar_item("Settings", "/settings", "settings"),
                    rx.spacer(height="2em"),
                    sidebar_item("Log out", "/logout", icon="log-out"),
                    spacing="1",
                    width="100%",
                ),
                rx.divider(),
                rx.hstack(
                    rx.icon_button(
                        rx.icon("user"),
                        size="3",
                        radius="full",
                    ),
                    rx.vstack(
                        rx.box(
                            rx.text(
                                "My account",
                                size="3",
                                weight="bold",
                            ),
                            rx.text(
                                "email",
                                size="2",
                                weight="medium",
                            ),
                            width="100%",
                        ),
                        spacing="0",
                        align="start",
                        justify="start",
                        width="100%",
                    ),
                    padding_x="0.5rem",
                    align="center",
                    justify="start",
                    width="100%",
                ),
                width="100%",
                spacing="5",
            ),
            sidebar_footer(),
            justify="space-between",
            align="stretch",
            width="100%",
            height="100%",
            spacing="4",
            padding_bottom="1em",
        ),
        **styles.sidebar_style,
    )