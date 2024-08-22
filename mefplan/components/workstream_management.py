import reflex as rx
from state.app_state import AppState


def workstream_management() -> rx.Component:
    return rx.vstack(
        rx.heading("Workstream Management", size="md"),
        rx.data_table(
            data=AppState.workstreams,
            columns=[
                {"header": "Name", "accessor": "workstream_name"},
                {"header": "Category", "accessor": "category"},
                {"header": "Description", "accessor": "description"},
            ],
        ),
        rx.dialog.root(
            rx.dialog.trigger(rx.button("Add Workstream")),
            rx.dialog.content(
                rx.dialog.title("Add Workstream"),
                rx.vstack(
                    rx.input(
                        placeholder="Workstream Name",
                        on_change=AppState.set_new_workstream_name,
                    ),
                    rx.select(
                        AppState.workstream_categories,
                        placeholder="Select Category",
                        on_change=AppState.set_new_workstream_category,
                    ),
                    rx.text_area(
                        placeholder="Description",
                        on_change=AppState.set_new_workstream_description,
                    ),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancel")),
                        rx.button("Add", on_click=AppState.add_workstream),
                    ),
                    spacing="4",
                ),
                size="3",
            ),
            open=AppState.workstream_modal_open,
            on_open_change=AppState.set_workstream_modal_open,
        ),
        width="100%",
    )
