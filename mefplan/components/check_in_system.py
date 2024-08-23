import reflex as rx
from ..state.app_state import AppState


def check_in_system() -> rx.Component:
    return rx.vstack(
        rx.heading("Check-In System", size="md"),
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Weekly"),
                rx.tabs.trigger("Bi-weekly"),
                rx.tabs.trigger("Monthly"),
                rx.tabs.trigger("End-of-month"),
            ),
            rx.tabs.content(
                "Weekly",
                rx.vstack(
                    rx.heading("Weekly Check-In", size="sm"),
                    rx.data_table(
                        data=AppState.weekly_check_ins,
                        columns=[
                            {"header": "Date", "accessor": "date"},
                            {"header": "Status", "accessor": "status"},
                        ],
                    ),
                    rx.button(
                        "Add Weekly Check-In",
                        on_click=AppState.open_weekly_check_in_modal,
                    ),
                ),
            ),
            rx.tabs.content(
                "Bi-weekly",
                rx.vstack(
                    rx.heading("Bi-Weekly Check-In", size="sm"),
                    rx.data_table(
                        data=AppState.biweekly_check_ins,
                        columns=[
                            {"header": "Date", "accessor": "date"},
                            {"header": "Status", "accessor": "status"},
                        ],
                    ),
                    rx.button(
                        "Add Bi-Weekly Check-In",
                        on_click=AppState.open_biweekly_check_in_modal,
                    ),
                ),
            ),
            rx.tabs.content(
                "Monthly",
                rx.vstack(
                    rx.heading("Monthly Check-In", size="sm"),
                    rx.data_table(
                        data=AppState.monthly_check_ins,
                        columns=[
                            {"header": "Date", "accessor": "date"},
                            {"header": "Status", "accessor": "status"},
                        ],
                    ),
                    rx.button(
                        "Add Monthly Check-In",
                        on_click=AppState.open_monthly_check_in_modal,
                    ),
                ),
            ),
            rx.tabs.content(
                "End-of-month",
                rx.vstack(
                    rx.heading("End-of-Month Check-In", size="sm"),
                    rx.data_table(
                        data=AppState.end_of_month_check_ins,
                        columns=[
                            {"header": "Date", "accessor": "date"},
                            {"header": "Status", "accessor": "status"},
                        ],
                    ),
                    rx.button(
                        "Add End-of-Month Check-In",
                        on_click=AppState.open_end_of_month_check_in_modal,
                    ),
                ),
            ),
        ),
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("Add Check-In"),
                rx.vstack(
                    rx.input(
                        type="date",
                        label="Date",
                        on_change=AppState.set_new_check_in_date,
                    ),
                    rx.text_area(
                        placeholder="Notes", on_change=AppState.set_new_check_in_notes
                    ),
                    rx.select(
                        ["Weekly", "Bi-weekly", "Monthly", "End-of-month"],
                        placeholder="Select Check-In Type",
                        on_change=AppState.set_new_check_in_type,
                    ),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancel")),
                        rx.button("Add", on_click=AppState.add_check_in),
                    ),
                    spacing="4",
                ),
                size="3",
            ),
            open=AppState.check_in_modal_open,
            on_open_change=AppState.set_check_in_modal_open,
        ),
        width="100%",
    )
