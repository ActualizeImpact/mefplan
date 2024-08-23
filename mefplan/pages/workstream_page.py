import reflex as rx
from ..backend.workstream_state import (
    WorkstreamState,
    WorkstreamBase,
    WorkstreamCategoryVar,
)
from ..templates import template
from ..components.workstream_stats_card import workstream_stats_card


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def show_workstream(workstream: WorkstreamBase, index: int) -> rx.Component:
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
        rx.table.row_header_cell(workstream.workstream_name),
        rx.table.cell(workstream.category),
        rx.table.cell(workstream.description or "N/A"),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(WorkstreamState.page_number),
            f" of {WorkstreamState.total_pages}",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=16),
                on_click=WorkstreamState.first_page,
                opacity=rx.cond(WorkstreamState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(
                    WorkstreamState.page_number == 1, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=16),
                on_click=WorkstreamState.prev_page,
                opacity=rx.cond(WorkstreamState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(
                    WorkstreamState.page_number == 1, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=16),
                on_click=WorkstreamState.next_page,
                opacity=rx.cond(
                    WorkstreamState.page_number == WorkstreamState.total_pages, 0.6, 1
                ),
                color_scheme=rx.cond(
                    WorkstreamState.page_number == WorkstreamState.total_pages,
                    "gray",
                    "accent",
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=16),
                on_click=WorkstreamState.last_page,
                opacity=rx.cond(
                    WorkstreamState.page_number == WorkstreamState.total_pages, 0.6, 1
                ),
                color_scheme=rx.cond(
                    WorkstreamState.page_number == WorkstreamState.total_pages,
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


def add_workstream_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Workstream", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="git-branch", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Workstream",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the workstream info",
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
                            rx.form.label("Workstream Name"),
                            rx.input(
                                placeholder="Enter workstream name",
                                name="workstream_name",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Description"),
                            rx.text_area(
                                placeholder="Enter description", name="description"
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Category"),
                            rx.select(
                                list(WorkstreamCategoryVar.__args__),
                                placeholder="Select category",
                                name="category",
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
                                rx.button("Add Workstream"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=WorkstreamState.handle_submit,
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
    route="/workstreams",
    title="Workstream Management",
    on_load=WorkstreamState.get_workstream_info(),
)
def workstream_page():
    return rx.vstack(
        rx.heading("Workstream Management", margin_bottom="1em"),
        rx.grid(
            workstream_stats_card(
                stat_name="Total Workstreams",
                value=WorkstreamState.total_workstreams,
                icon="git-branch",
                icon_color="blue",
            ),
            *[
                workstream_stats_card(
                    stat_name=category,
                    value=WorkstreamState.workstreams_by_category[category],
                    icon="folder",
                    icon_color="accent",
                )
                for category in WorkstreamCategoryVar.__args__
            ],
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(2, 1fr)",
                "repeat(3, 1fr)",
                "repeat(4, 1fr)",
            ],
            width="100%",
            margin_bottom="1em",
        ),
        rx.flex(
            add_workstream_dialog(),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    WorkstreamState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=WorkstreamState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=WorkstreamState.toggle_sort,
                    ),
                ),
                rx.select(
                    ["workstream_name", "category", "description"],
                    placeholder="Sort By: Workstream Name",
                    size="3",
                    on_change=WorkstreamState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=WorkstreamState.clear_search,
                        display=rx.cond(WorkstreamState.search_value, "flex", "none"),
                    ),
                    value=WorkstreamState.search_value,
                    placeholder="Search workstreams...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=WorkstreamState.set_search_value,
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
                        _header_cell("Workstream Name", "git-branch"),
                        _header_cell("Category", "folder"),
                        _header_cell("Description", "file-text"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        WorkstreamState.current_page_workstreams,
                        lambda workstream, index: show_workstream(workstream, index),
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
