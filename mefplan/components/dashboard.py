import reflex as rx
from ..state.app_state import AppState
from ..dashboard_styles import apply_dashboard_style


def dashboard() -> rx.Component:
    return apply_dashboard_style(
        rx.vstack(
            rx.heading("Dashboard", size="lg", mb="4"),
            rx.grid(
                rx.foreach(
                    [
                        {
                            "title": "Total Tasks",
                            "content": rx.vstack(
                                rx.text(
                                    AppState.total_tasks,
                                    font_size="2xl",
                                    font_weight="bold",
                                ),
                                rx.heading("Tasks by Status", size="sm", mt="4"),
                                rx.recharts.pie_chart(
                                    rx.recharts.pie(
                                        data=AppState.tasks_by_status,
                                        data_key="value",
                                        name_key="name",
                                        cx="50%",
                                        cy="50%",
                                        label=rx.recharts.label(
                                            position="inside", offset=20
                                        ),
                                    ),
                                    width="100%",
                                    height=250,
                                ),
                            ),
                            "col_span": 1,
                        },
                        {
                            "title": "Workstream Progress",
                            "content": rx.recharts.bar_chart(
                                rx.recharts.bar(
                                    data=AppState.workstream_progress,
                                    data_key="progress",
                                    name_key="workstream",
                                ),
                                width="100%",
                                height=250,
                            ),
                            "col_span": 1,
                        },
                        {
                            "title": "Upcoming Milestones",
                            "content": rx.data_table(
                                data=AppState.upcoming_milestones,
                                columns=[
                                    {
                                        "header": "Milestone",
                                        "accessor": "milestone_name",
                                    },
                                    {
                                        "header": "Target Date",
                                        "accessor": "target_date",
                                    },
                                ],
                            ),
                            "col_span": 2,
                        },
                        {
                            "title": "Staff Workload",
                            "content": rx.recharts.bar_chart(
                                rx.recharts.bar(
                                    data=AppState.staff_workload,
                                    data_key="tasks",
                                    name_key="staff",
                                ),
                                layout="vertical",
                                width="100%",
                                height=250,
                            ),
                            "col_span": 1,
                        },
                        {
                            "title": "Recent Activity",
                            "content": rx.scroll_area(
                                rx.vstack(
                                    rx.foreach(
                                        AppState.recent_activity, lambda a: rx.text(a)
                                    ),
                                    spacing="2",
                                ),
                                height="200px",
                            ),
                            "col_span": 1,
                        },
                    ],
                    lambda item: rx.box(
                        rx.card(
                            rx.vstack(
                                rx.heading(item["title"], size="md"),
                                item["content"],
                            ),
                            height="100%",
                        ),
                        grid_column=f"span {item['col_span']} / span {item['col_span']}",
                    ),
                ),
                template_columns="repeat(2, 1fr)",
                gap="4",
                width="100%",
            ),
            width="100%",
            spacing="4",
        )
    )
