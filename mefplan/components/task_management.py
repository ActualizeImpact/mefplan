import reflex as rx
from ..state.app_state import AppState


def task_management() -> rx.Component:
    return rx.vstack(
        rx.heading("Task Management", size="md"),
        rx.data_table(
            data=AppState.tasks,
            columns=[
                {"header": "Task Name", "accessor": "task_name"},
                {"header": "Status", "accessor": "status"},
                {"header": "Priority", "accessor": "priority"},
                {"header": "Start Date", "accessor": "start_date"},
                {"header": "End Date", "accessor": "end_date"},
                {"header": "Assigned To", "accessor": "assigned_to"},
            ],
        ),
        rx.dialog.root(
            rx.dialog.trigger(rx.button("Add Task")),
            rx.dialog.content(
                rx.dialog.title("Add Task"),
                rx.vstack(
                    rx.input(
                        placeholder="Task Name", on_change=AppState.set_new_task_name
                    ),
                    rx.select(
                        AppState.task_statuses,
                        placeholder="Select Status",
                        on_change=AppState.set_new_task_status,
                    ),
                    rx.select(
                        AppState.task_priorities,
                        placeholder="Select Priority",
                        on_change=AppState.set_new_task_priority,
                    ),
                    rx.input(
                        type="date",
                        label="Start Date",
                        on_change=AppState.set_new_task_start_date,
                    ),
                    rx.input(
                        type="date",
                        label="End Date",
                        on_change=AppState.set_new_task_end_date,
                    ),
                    rx.select(
                        AppState.staff_members,
                        placeholder="Assign To",
                        on_change=AppState.set_new_task_assigned_to,
                    ),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancel")),
                        rx.button("Add", on_click=AppState.add_task),
                    ),
                    spacing="4",
                ),
                size="3",
            ),
            open=AppState.task_modal_open,
            on_open_change=AppState.set_task_modal_open,
        ),
        width="100%",
    )
