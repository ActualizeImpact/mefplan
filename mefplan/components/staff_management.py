import reflex as rx
from ..state.app_state import AppState


def staff_management() -> rx.Component:
    return rx.vstack(
        rx.heading("Staff Management", size="md"),
        rx.data_table(
            data=AppState.staff_members,
            columns=[
                {"header": "First Name", "accessor": "first_name"},
                {"header": "Last Name", "accessor": "last_name"},
                {"header": "Role", "accessor": "role"},
                {"header": "Email", "accessor": "email"},
                {"header": "Phone", "accessor": "phone"},
            ],
        ),
        rx.dialog.root(
            rx.dialog.trigger(rx.button("Add Staff Member")),
            rx.dialog.content(
                rx.dialog.title("Add Staff Member"),
                rx.vstack(
                    rx.input(
                        placeholder="First Name",
                        on_change=AppState.set_new_staff_first_name,
                    ),
                    rx.input(
                        placeholder="Last Name",
                        on_change=AppState.set_new_staff_last_name,
                    ),
                    rx.input(placeholder="Role", on_change=AppState.set_new_staff_role),
                    rx.input(
                        placeholder="Email",
                        type="email",
                        on_change=AppState.set_new_staff_email,
                    ),
                    rx.input(
                        placeholder="Phone",
                        type="tel",
                        on_change=AppState.set_new_staff_phone,
                    ),
                    rx.multi_select(
                        AppState.workstreams,
                        placeholder="Assign Workstreams",
                        on_change=AppState.set_new_staff_workstreams,
                    ),
                    rx.hstack(
                        rx.dialog.close(rx.button("Cancel")),
                        rx.button("Add", on_click=AppState.add_staff_member),
                    ),
                    spacing="4",
                ),
                size="3",
            ),
            open=AppState.staff_modal_open,
            on_open_change=AppState.set_staff_modal_open,
        ),
        width="100%",
    )
