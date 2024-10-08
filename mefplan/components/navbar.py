"""Navbar component for the app."""

from .. import styles

import reflex as rx


def menu_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=20)


def menu_item(text: str, url: str) -> rx.Component:
    """Menu item.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The menu item component.
    """
    # Whether the item is active.
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & (text == "Dashboard")
    )

    return rx.link(
        rx.hstack(
            rx.match(
                text,
                ("Dashboard", menu_item_icon("gauge")),
                ("Tasks", menu_item_icon("clipboard-list")),
                ("Workstreams", menu_item_icon("git-branch")),
                ("Milestones", menu_item_icon("flag")),
                ("Check-ins", menu_item_icon("check-circle")),
                ("Meetings", menu_item_icon("users")),
                ("Black Business Finder", menu_item_icon("search")),
            ),
            rx.text(text, size="4", weight="regular"),
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


def navbar_footer() -> rx.Component:
    """Navbar footer.

    Returns:
        The navbar footer component.
    """
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


def menu_button(hidden_routes: list[str] = None) -> rx.Component:
    # Get all the decorated pages and add them to the menu.
    from reflex.page import get_decorated_pages

    # The ordered page routes.
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

    # Get the decorated pages.
    pages = get_decorated_pages()

    # Include all pages even if they are not in the ordered_page_routes.
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

    return rx.drawer.root(
        rx.drawer.trigger(
            rx.icon("align-justify"),
        ),
        rx.drawer.overlay(z_index="5"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.hstack(
                        rx.spacer(),
                        rx.drawer.close(rx.icon(tag="x")),
                        justify="end",
                        width="100%",
                    ),
                    rx.divider(),
                    *[
                        menu_item(
                            text=page.get(
                                "title", page["route"].strip("/").capitalize()
                            ),
                            url=page["route"],
                        )
                        for page in visible_pages
                    ],
                    rx.spacer(),
                    navbar_footer(),
                    spacing="4",
                    width="100%",
                ),
                top="auto",
                left="auto",
                height="100%",
                width="20em",
                padding="1em",
                bg=rx.color("gray", 1),
            ),
            width="100%",
        ),
        direction="right",
    )


def navbar(hidden_routes: list[str] = None) -> rx.Component:
    """The navbar.

    Args:
        hidden_routes: List of routes to hide from the navbar.

    Returns:
        The navbar component.
    """
    return rx.box(
        rx.hstack(
            rx.color_mode_cond(
                rx.image(src="/CEP_W.png", height=["2em", "2.25em", "2.5em"]),
                rx.image(src="/CEP_W.png", height="5em"),
            ),
            rx.spacer(),
            menu_button(hidden_routes=hidden_routes),
            **styles.navbar_content_style,
        ),
        **styles.navbar_style,
    )