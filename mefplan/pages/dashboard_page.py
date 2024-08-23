import reflex as rx
from ..backend.dashboard_state import DashboardState
from ..components.dashboard_components import (
    dashboard_stats_card,
    area_toggle,
    tasks_chart,
    workstream_progress_chart,
    staff_workload_chart,
    card,
)
from ..templates import template


@template(
    route="/dashboard",
    title="Project Dashboard",
    on_load=DashboardState.fetch_data(),
)
def dashboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Project Dashboard", size="5"),
        rx.flex(
            rx.input(
                rx.input.slot(rx.icon("search"), padding_left="0"),
                placeholder="Search here...",
                size="3",
                width="100%",
                max_width="450px",
                radius="large",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        rx.grid(
            dashboard_stats_card(
                stat_name="Total Tasks",
                value=DashboardState.total_tasks,
                icon="clipboard-list",
                icon_color="blue",
            ),
            dashboard_stats_card(
                stat_name="Completed Tasks",
                value=DashboardState.tasks_by_status[2].value,
                icon="check-circle",
                icon_color="green",
            ),
            dashboard_stats_card(
                stat_name="In Progress Tasks",
                value=DashboardState.tasks_by_status[1].value,
                icon="clock",
                icon_color="yellow",
            ),
            dashboard_stats_card(
                stat_name="Not Started Tasks",
                value=DashboardState.tasks_by_status[0].value,
                icon="alert-circle",
                icon_color="red",
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
                "repeat(4, 1fr)",
            ],
            width="100%",
            margin_bottom="1em",
        ),
        card(
            rx.hstack(
                rx.hstack(
                    rx.icon("bar-chart-2", size=20),
                    rx.text("Tasks Overview", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                ),
                area_toggle(),
                width="100%",
                justify="between",
            ),
            tasks_chart(),
        ),
        rx.grid(
            card(
                rx.hstack(
                    rx.icon("git-branch", size=20),
                    rx.text("Workstream Progress", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                    margin_bottom="1em",
                ),
                workstream_progress_chart(),
            ),
            card(
                rx.hstack(
                    rx.icon("users", size=20),
                    rx.text("Staff Workload", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                    margin_bottom="1em",
                ),
                staff_workload_chart(),
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
            ],
            width="100%",
        ),
        card(
            rx.hstack(
                rx.icon("calendar", size=20),
                rx.text("Upcoming Milestones", size="4", weight="medium"),
                align="center",
                spacing="2",
                margin_bottom="1em",
            ),
            rx.data_table(
                data=DashboardState.upcoming_milestones,
                pagination=True,
                search=True,
                sort=True,
            ),
        ),
        card(
            rx.hstack(
                rx.icon("activity", size=20),
                rx.text("Recent Activity", size="4", weight="medium"),
                align="center",
                spacing="2",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.foreach(
                    DashboardState.recent_activity,
                    lambda activity: rx.text(activity),
                ),
                spacing="2",
            ),
        ),
        spacing="8",
        width="100%",
    )
