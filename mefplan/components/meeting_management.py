import reflex as rx
from ..state.app_state import AppState


def meeting_management() -> rx.Component:
    return rx.vstack(
        rx.heading("Meeting Management", size="md"),
        rx.data_table(
            data=AppState.meetings,
            columns=[
                {"header": "Meeting Name", "accessor": "meeting_name"},
                {"header": "Date", "accessor": "date"},
                {"header": "Time", "accessor": "time"},
                {"header": "Attendees", "accessor": "attendees"},
            ],
        ),
        rx.dialog.root(
            rx.dialog.trigger(rx.button("Schedule Meeting")),
            rx.dialog.content(
                rx.dialog.title("Schedule Meeting"),
                rx.vstack(
                    rx.input(
                        placeholder="Meeting Name",
                        on_change=AppState.set_new_meeting_name,
                    ),
                    rx.input(
                        type="date",
                        label="Date",
                        on_change=AppState.set_new_meeting_date,
                    ),
                    rx.input(
                        type="time",
                        label="Time",
                        on_change=AppState.set_new_meeting_time,
                    ),
                    rx.multi_select(
                        AppState.staff_members,
                        placeholder="Select Attendees",
                        on_change=AppState.set_new_meeting_attendees,
                    ),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancel")),
                        rx.button("Schedule", on_click=AppState.add_meeting),
                    ),
                    spacing="4",
                ),
                size="3",
            ),
            open=AppState.meeting_modal_open,
            on_open_change=AppState.set_meeting_modal_open,
        ),
        width="100%",
    )
