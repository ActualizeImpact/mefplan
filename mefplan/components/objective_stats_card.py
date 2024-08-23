import reflex as rx
from .. import styles
from reflex.components.radix.themes.base import LiteralAccentColor


def objective_stats_card(
    stat_name: str,
    value: rx.Var,
    icon: str,
    icon_color: LiteralAccentColor,
) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(tag=icon, size=34),
                    color_scheme=icon_color,
                    radius="full",
                    padding="0.7rem",
                ),
                rx.vstack(
                    rx.heading(
                        rx.cond(value > 999, f"{value / 1000:.1f}k", f"{value}"),
                        size="6",
                        weight="bold",
                    ),
                    rx.text(stat_name, size="4", weight="medium"),
                    spacing="1",
                    height="100%",
                    align_items="start",
                    width="100%",
                ),
                height="100%",
                spacing="4",
                align="center",
                width="100%",
            ),
            spacing="3",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
    )