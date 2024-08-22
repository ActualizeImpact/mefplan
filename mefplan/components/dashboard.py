import reflex as rx
from state.app_state import AppState

def dashboard() -> rx.Component:
    return rx.vstack(
        rx.heading("Dashboard", size="md"),
        rx.flex(
            rx.vstack(
                rx.heading("Total Tasks", size="sm"),
                rx.text(AppState.total_tasks),
                rx.heading("Tasks by Status", size="sm"),
                rx.pie_chart(
                    rx.pie(
                        data=AppState.tasks_by_status,
                        data_key="value",
                        name_key="name",
                        cx="50%",
                        cy="50%",
                        label=rx.label(position="inside", offset=20),
                    ),
                    width=300,
                    height=300,
                ),
            ),
            rx.vstack(
                rx.heading("Upcoming Milestones", size="sm"),
                rx.data_table(
                    data=AppState.upcoming_milestones,
                    columns=[
                        {"header": "Milestone", "accessor": "milestone_name"},
                        {"header": "Target Date", "accessor": "target_date"},
                    ],
                ),
            ),
            rx.vstack(
                rx.heading("Recent Activity", size="sm"),
                rx.foreach(AppState.recent_activity, lambda a: rx.text(a)),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
    )
