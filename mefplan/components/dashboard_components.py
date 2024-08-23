import reflex as rx
from ..backend.dashboard_state import DashboardState
from .. import styles
from reflex.components.radix.themes.base import LiteralAccentColor


def dashboard_stats_card(
    stat_name: str,
    value: rx.Var,
    icon: str,
    icon_color: str,
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


def area_toggle() -> rx.Component:
    return rx.cond(
        DashboardState.area_toggle,
        rx.icon_button(
            rx.icon("area-chart"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=DashboardState.toggle_areachart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=DashboardState.toggle_areachart,
        ),
    )


def _create_gradient(color: LiteralAccentColor, id: str) -> rx.Component:
    return (
        rx.el.svg.defs(
            rx.el.svg.linear_gradient(
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="5%", stop_opacity=0.8
                ),
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="95%", stop_opacity=0
                ),
                x1=0,
                x2=0,
                y1=0,
                y2=1,
                id=id,
            ),
        ),
    )


def _custom_tooltip(color: LiteralAccentColor) -> rx.Component:
    return (
        rx.recharts.graphing_tooltip(
            separator=" : ",
            content_style={
                "backgroundColor": rx.color("gray", 1),
                "borderRadius": "var(--radius-2)",
                "borderWidth": "1px",
                "borderColor": rx.color(color, 7),
                "padding": "0.5rem",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
            },
            is_animation_active=True,
        ),
    )


def tasks_chart() -> rx.Component:
    return rx.cond(
        DashboardState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("blue", "colorBlue"),
            _custom_tooltip("blue"),
            rx.recharts.area(
                data_key="value",
                stroke=rx.color("blue", 9),
                fill="url(#colorBlue)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            data=DashboardState.tasks_by_status,
            height=300,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("blue"),
            rx.recharts.bar(
                data_key="value",
                fill=rx.color("blue", 7),
            ),
            rx.recharts.x_axis(data_key="name"),
            rx.recharts.y_axis(),
            data=DashboardState.tasks_by_status,
            height=300,
        ),
    )


def workstream_progress_chart() -> rx.Component:
    return rx.recharts.bar_chart(
        _custom_tooltip("green"),
        rx.recharts.bar(
            data_key="progress",
            fill=rx.color("green", 7),
        ),
        rx.recharts.x_axis(data_key="workstream"),
        rx.recharts.y_axis(),
        data=DashboardState.workstream_progress,
        height=250,
    )


def staff_workload_chart() -> rx.Component:
    return rx.recharts.bar_chart(
        _custom_tooltip("purple"),
        rx.recharts.bar(
            data_key="tasks",
            fill=rx.color("purple", 7),
        ),
        rx.recharts.x_axis(data_key="staff"),
        rx.recharts.y_axis(),
        layout="vertical",
        data=DashboardState.staff_workload,
        height=250,
    )


def card(*children, **props):
    return rx.card(
        *children,
        box_shadow=styles.box_shadow_style,
        size="3",
        width="100%",
        **props,
    )
