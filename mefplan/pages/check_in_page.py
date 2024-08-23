import reflex as rx
from ..backend.check_in_state import CheckInState, CheckInBase, CheckInTypeEnum, CheckInStatusEnum
from ..templates import template
from ..components.check_in_stats_card import check_in_stats_card


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def show_check_in(check_in: CheckInBase, index: int) -> rx.Component:
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
        rx.table.row_header_cell(check_in.check_in_type),
        rx.table.cell(check_in.date),
        rx.table.cell(check_in.status),
        rx.table.cell(check_in.notes),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(CheckInState.page_number),
            f" of {CheckInState.total_pages}",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=16),
                on_click=CheckInState.first_page,
                opacity=rx.cond(CheckInState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(CheckInState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=16),
                on_click=CheckInState.prev_page,
                opacity=rx.cond(CheckInState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(CheckInState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=16),
                on_click=CheckInState.next_page,
                opacity=rx.cond(
                    CheckInState.page_number == CheckInState.total_pages, 0.6, 1
                ),
                color_scheme=rx.cond(
                    CheckInState.page_number == CheckInState.total_pages,
                    "gray",
                    "accent",
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=16),
                on_click=CheckInState.last_page,
                opacity=rx.cond(
                    CheckInState.page_number == CheckInState.total_pages, 0.6, 1
                ),
                color_scheme=rx.cond(
                    CheckInState.page_number == CheckInState.total_pages,
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


def add_check_in_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Check-In", size="4", display=["none", "none", "block"]),
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
                        "Add New Check-In",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the check-in info",
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
                            rx.form.label("Check-In Type"),
                            rx.select(
                                CheckInTypeEnum.__args__,
                                placeholder="Select check-in type",
                                name="check_in_type",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Date"),
                            rx.input(
                                type="date",
                                name="date",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Status"),
                            rx.select(
                                CheckInStatusEnum.__args__,
                                placeholder="Select status",
                                name="status",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Notes"),
                            rx.text_area(
                                placeholder="Enter notes",
                                name="notes",
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
                                rx.button("Add Check-In"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=CheckInState.add_check_in_to_db,
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
    route="/check-ins",
    title="Check-In System",
    on_load=CheckInState.get_check_in_info(),
)
def check_in_page():
    return rx.vstack(
        rx.heading("Check-In Information", margin_bottom="1em"),
        rx.grid(
            check_in_stats_card(
                stat_name="Total Check-Ins",
                value=CheckInState.total_check_ins,
                icon="calendar",
                icon_color="blue",
            ),
            check_in_stats_card(
                stat_name="Weekly Check-Ins",
                value=CheckInState.check_ins_by_type["Weekly"],
                icon="calendar-check",
                icon_color="pink",
            ),
            check_in_stats_card(
                stat_name="Monthly Check-Ins",
                value=CheckInState.check_ins_by_type["Monthly"],
                icon="calendar-days",
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
            add_check_in_dialog(),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    CheckInState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=CheckInState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=CheckInState.toggle_sort,
                    ),
                ),
                rx.select(
                    ["check_in_type", "date", "status"],
                    placeholder="Sort By: Date",
                    size="3",
                    on_change=CheckInState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=CheckInState.set_search_value(""),
                        display=rx.cond(CheckInState.search_value, "flex", "none"),
                    ),
                    value=CheckInState.search_value,
                    placeholder="Search here...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=CheckInState.set_search_value,
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
                        _header_cell("Type", "calendar"),
                        _header_cell("Date", "calendar-days"),
                        _header_cell("Status", "check-circle"),
                        _header_cell("Notes", "file-text"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        CheckInState.current_page_check_ins,
                        lambda check_in, index: show_check_in(check_in, index),
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
