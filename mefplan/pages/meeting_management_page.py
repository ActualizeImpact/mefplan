import reflex as rx
from ..backend.meeting_management_state import MeetingState, Meeting
from ..templates import template
from ..components.meeting_management_stats_card import meeting_stats_card


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def show_meeting(meeting: Meeting, index: int) -> rx.Component:
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
        rx.table.row_header_cell(meeting.meeting_title),
        rx.table.cell(meeting.meeting_date),
        rx.table.cell(meeting.participants),
        rx.table.cell(meeting.meeting_notes),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(MeetingState.page_number),
            f" of {MeetingState.total_pages}",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=16),
                on_click=MeetingState.first_page,
                opacity=rx.cond(MeetingState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(MeetingState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=16),
                on_click=MeetingState.prev_page,
                opacity=rx.cond(MeetingState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(MeetingState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=16),
                on_click=MeetingState.next_page,
                opacity=rx.cond(MeetingState.page_number == MeetingState.total_pages, 0.6, 1),
                color_scheme=rx.cond(
                    MeetingState.page_number == MeetingState.total_pages, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=16),
                on_click=MeetingState.last_page,
                opacity=rx.cond(MeetingState.page_number == MeetingState.total_pages, 0.6, 1),
                color_scheme=rx.cond(
                    MeetingState.page_number == MeetingState.total_pages, "gray", "accent"
                ),
                variant="soft",
            ),
            spacing="1",
        ),
        width="100%",
        padding_top="0.5em",
    )


def add_meeting_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Schedule Meeting", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="calendar", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Schedule Meeting",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the meeting details",
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
                            rx.form.label("Meeting Title"),
                            rx.input(
                                placeholder="Enter meeting title",
                                name="meeting_title",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Date"),
                            rx.input(
                                type="date",
                                name="meeting_date",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Participants"),
                            rx.input(
                                placeholder="Enter participants",
                                name="participants",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Notes"),
                            rx.text_area(
                                placeholder="Enter meeting notes",
                                name="meeting_notes",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Workstream ID"),
                            rx.input(
                                placeholder="Enter workstream ID",
                                name="workstream_id",
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
                                rx.button("Schedule Meeting"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=MeetingState.add_meeting,
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
    route="/meetings",
    title="Meeting Management",
    on_load=MeetingState.get_meeting_info(),
)
def meeting_management_page():
    return rx.vstack(
        rx.heading("Meeting Management", size="md", margin_bottom="1em"),
        rx.grid(
            meeting_stats_card(
                stat_name="Total Meetings",
                value=MeetingState.total_meetings,
                icon="calendar",
                icon_color="blue",
            ),
            meeting_stats_card(
                stat_name="Upcoming Meetings",
                value=MeetingState.upcoming_meetings,
                icon="calendar-check",
                icon_color="pink",
            ),
            meeting_stats_card(
                stat_name="Past Meetings",
                value=MeetingState.past_meetings,
                icon="calendar-x",
                icon_color="grass",
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
            add_meeting_dialog(),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    MeetingState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=MeetingState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=MeetingState.toggle_sort,
                    ),
                ),
                rx.select(
                    ["meeting_title", "meeting_date", "participants"],
                    placeholder="Sort By: Meeting Title",
                    size="3",
                    on_change=MeetingState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=MeetingState.clear_search,
                        display=rx.cond(MeetingState.search_value, "flex", "none"),
                    ),
                    value=MeetingState.search_value,
                    placeholder="Search here...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=MeetingState.set_search_value,
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
                        _header_cell("Meeting Title", "calendar"),
                        _header_cell("Date", "calendar-days"),
                        _header_cell("Participants", "users"),
                        _header_cell("Notes", "file-text"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        MeetingState.current_page_meetings,
                        lambda meeting, index: show_meeting(meeting, index),
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