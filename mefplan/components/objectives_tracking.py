import reflex as rx
from ..state.app_state import AppState


def objectives_tracking() -> rx.Component:
    return rx.vstack(
        rx.heading("Objectives Tracking", size="md"),
        rx.data_table(
            data=AppState.objectives,
            columns=[
                {"header": "Objective Name", "accessor": "objective_name"},
                {"header": "Description", "accessor": "description"},
                {"header": "Workstream", "accessor": "workstream_id"},
                {"header": "Target Date", "accessor": "target_date"},
                {"header": "Status", "accessor": "status"},
            ],
        ),
        rx.dialog.root(
            rx.dialog.trigger(rx.button("Add Objective")),
            rx.dialog.content(
                rx.dialog.title("Add Objective"),
                rx.vstack(
                    rx.input(
                        placeholder="Objective Name",
                        on_change=AppState.set_new_objective_name,
                    ),
                    rx.text_area(
                        placeholder="Description",
                        on_change=AppState.set_new_objective_description,
                    ),
                    rx.select(
                        AppState.workstreams,
                        placeholder="Select Workstream",
                        on_change=AppState.set_new_objective_workstream,
                    ),
                    rx.input(
                        type="date",
                        label="Target Date",
                        on_change=AppState.set_new_objective_target_date,
                    ),
                    rx.select(
                        AppState.milestone_statuses,
                        placeholder="Select Status",
                        on_change=AppState.set_new_objective_status,
                    ),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancel")),
                        rx.button("Add", on_click=AppState.add_objective),
                    ),
                    spacing="4",
                ),
                size="3",
            ),
            open=AppState.objective_modal_open,
            on_open_change=AppState.set_objective_modal_open,
        ),
        width="100%",
    )
