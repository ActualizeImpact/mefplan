import reflex as rx
from ..state.app_state import AppState


def milestone_tracker() -> rx.Component:
    return rx.vstack(
        rx.heading("Milestone Tracker", size="md"),
        rx.data_table(
            data=AppState.milestones,
            columns=[
                {"header": "Milestone Name", "accessor": "milestone_name"},
                {"header": "Target Date", "accessor": "target_date"},
                {"header": "Status", "accessor": "status"},
                {"header": "Workstream", "accessor": "workstream_id"},
            ],
        ),
        rx.dialog.root(
            rx.dialog.trigger(rx.button("Add Milestone")),
            rx.dialog.content(
                rx.dialog.title("Add Milestone"),
                rx.vstack(
                    rx.input(
                        placeholder="Milestone Name",
                        on_change=AppState.set_new_milestone_name,
                    ),
                    rx.input(
                        type="date",
                        label="Target Date",
                        on_change=AppState.set_new_milestone_target_date,
                    ),
                    rx.select(
                        AppState.milestone_statuses,
                        placeholder="Select Status",
                        on_change=AppState.set_new_milestone_status,
                    ),
                    rx.select(
                        AppState.workstreams,
                        placeholder="Select Workstream",
                        on_change=AppState.set_new_milestone_workstream,
                    ),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancel")),
                        rx.button("Add", on_click=AppState.add_milestone),
                    ),
                    spacing="4",
                ),
                size="3",
            ),
            open=AppState.milestone_modal_open,
            on_open_change=AppState.set_milestone_modal_open,
        ),
        width="100%",
    )
