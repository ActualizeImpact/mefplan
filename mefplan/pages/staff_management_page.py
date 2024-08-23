import reflex as rx
from ..backend.staff_management_state import StaffManagementState, StaffMemberBase
from ..templates import template
from ..components.staff_management_stats_card import staff_stats_card


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def show_staff_member(staff_member: StaffMemberBase, index: int) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),
    )
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),
    )
    return rx.table.row(
        rx.table.row_header_cell(f"{staff_member.first_name} {staff_member.last_name}"),
        rx.table.cell(staff_member.role),
        rx.table.cell(staff_member.email),
        rx.table.cell(staff_member.phone or "N/A"),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(StaffManagementState.page_number),
            f" of {StaffManagementState.total_pages}",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=16),
                on_click=StaffManagementState.first_page,
                opacity=rx.cond(StaffManagementState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(
                    StaffManagementState.page_number == 1, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=16),
                on_click=StaffManagementState.prev_page,
                opacity=rx.cond(StaffManagementState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(
                    StaffManagementState.page_number == 1, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=16),
                on_click=StaffManagementState.next_page,
                opacity=rx.cond(
                    StaffManagementState.page_number
                    == StaffManagementState.total_pages,
                    0.6,
                    1,
                ),
                color_scheme=rx.cond(
                    StaffManagementState.page_number
                    == StaffManagementState.total_pages,
                    "gray",
                    "accent",
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=16),
                on_click=StaffManagementState.last_page,
                opacity=rx.cond(
                    StaffManagementState.page_number
                    == StaffManagementState.total_pages,
                    0.6,
                    1,
                ),
                color_scheme=rx.cond(
                    StaffManagementState.page_number
                    == StaffManagementState.total_pages,
                    "gray",
                    "accent",
                ),
                variant="soft",
            ),
            spacing="1",
        ),
        width="100%",
        padding_top="0.5em",
    )


def add_staff_member_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text(
                    "Add Staff Member", size="4", display=["none", "none", "block"]
                ),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="user", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Staff Member",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the staff member's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        rx.form.field(
                            rx.form.label("First Name"),
                            rx.input(placeholder="Enter first name", name="first_name"),
                        ),
                        rx.form.field(
                            rx.form.label("Last Name"),
                            rx.input(placeholder="Enter last name", name="last_name"),
                        ),
                        rx.form.field(
                            rx.form.label("Role"),
                            rx.input(placeholder="Enter role", name="role"),
                        ),
                        rx.form.field(
                            rx.form.label("Email"),
                            rx.input(
                                placeholder="Enter email", name="email", type_="email"
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Phone"),
                            rx.input(
                                placeholder="Enter phone number",
                                name="phone",
                                type_="tel",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Assigned Workstreams"),
                            rx.number_input(
                                placeholder="Enter workstream IDs",
                                name="assigned_workstream_ids",
                            ),
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Add Staff Member"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=StaffManagementState.handle_submit,
                    reset_on_submit=True,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


@template(
    route="/staff",
    title="Staff Management",
    on_load=StaffManagementState.get_staff_info(),
)
def staff_management_page():
    return rx.vstack(
        rx.heading("Staff Management", margin_bottom="1em"),
        rx.grid(
            staff_stats_card(
                stat_name="Total Staff",
                value=StaffManagementState.total_staff_members,
                icon="users",
                icon_color="blue",
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(3, 1fr)",
                "repeat(3, 1fr)",
            ],
            width="100%",
            margin_bottom="1em",
        ),
        rx.flex(
            add_staff_member_dialog(),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    StaffManagementState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=StaffManagementState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=StaffManagementState.toggle_sort,
                    ),
                ),
                rx.select(
                    ["first_name", "last_name", "role", "email"],
                    placeholder="Sort By: First Name",
                    size="3",
                    on_change=StaffManagementState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=StaffManagementState.clear_search,
                        display=rx.cond(
                            StaffManagementState.search_value, "flex", "none"
                        ),
                    ),
                    value=StaffManagementState.search_value,
                    placeholder="Search staff...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=StaffManagementState.set_search_value,
                ),
                align="center",
                justify="end",
                spacing="3",
            ),
            spacing="3",
            justify="between",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        _header_cell("Name", "user"),
                        _header_cell("Role", "briefcase"),
                        _header_cell("Email", "mail"),
                        _header_cell("Phone", "phone"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        StaffManagementState.current_page_staff_members,
                        lambda staff_member, index: show_staff_member(
                            staff_member, index
                        ),
                    )
                ),
                variant="surface",
                size="3",
                width="100%",
            ),
            overflow_x="auto",
            width="100%",
        ),
        _pagination_view(),
        width="100%",
        spacing="4",
        align_items="stretch",
        height="100%",
        overflow_y="auto",
    )
