import reflex as rx
from ..backend.milestone_state import MilestoneState, MilestoneBase, MilestoneStatusVar
from ..templates import template
from ..components.milestone_stats_card import milestone_stats_card


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def show_milestone(milestone: MilestoneBase, index: int) -> rx.Component:
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
        rx.table.row_header_cell(milestone.milestone_name),
        rx.table.cell(milestone.target_date),
        rx.table.cell(milestone.status),
        rx.table.cell(str(milestone.workstream_id)),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(MilestoneState.page_number),
            f" of {MilestoneState.total_pages}",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=16),
                on_click=MilestoneState.first_page,
                opacity=rx.cond(MilestoneState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(MilestoneState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=16),
                on_click=MilestoneState.prev_page,
                opacity=rx.cond(MilestoneState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(MilestoneState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=16),
                on_click=MilestoneState.next_page,
                opacity=rx.cond(MilestoneState.page_number == MilestoneState.total_pages, 0.6, 1),
                color_scheme=rx.cond(
                    MilestoneState.page_number == MilestoneState.total_pages, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=16),
                on_click=MilestoneState.last_page,
                opacity=rx.cond(MilestoneState.page_number == MilestoneState.total_pages, 0.6, 1),
                color_scheme=rx.cond(
                    MilestoneState.page_number == MilestoneState.total_pages, "gray", "accent"
                ),
                variant="soft",
            ),
            spacing="1",
        ),
        width="100%",
        padding_top="0.5em",
    )


def add_milestone_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Milestone", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="flag", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Milestone",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the milestone info",
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
                            rx.form.label("Milestone Name"),
                            rx.input(
                                placeholder="Enter milestone name", name="milestone_name"
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Target Date"),
                            rx.input(type_="date", name="target_date"),
                        ),
                        rx.form.field(
                            rx.form.label("Status"),
                            rx.select(
                                list(MilestoneStatusVar.__args__),
                                placeholder="Select status",
                                name="status",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Workstream ID"),
                            rx.input(placeholder="Enter workstream ID", name="workstream_id"),
                        ),
                        rx.form.field(
                            rx.form.label("Objective ID"),
                            rx.input(placeholder="Enter objective ID (optional)", name="objective_id"),
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
                                rx.button("Add Milestone"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=MilestoneState.handle_submit,
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
    route="/milestones",
    title="Milestone Management",
    on_load=MilestoneState.get_milestone_info(),
)
def milestone_page():
    return rx.vstack(
        rx.heading("Milestone Management", margin_bottom="1em"),
        rx.grid(
            milestone_stats_card(
                stat_name="Total Milestones",
                value=MilestoneState.total_milestones,
                icon="flag",
                icon_color="blue",
            ),
            milestone_stats_card(
                stat_name="Not Started",
                value=MilestoneState.milestones_by_status["Not Started"],
                icon="circle",
                icon_color="red",
            ),
            milestone_stats_card(
                stat_name="In Progress",
                value=MilestoneState.milestones_by_status["In Progress"],
                icon="clock",
                icon_color="yellow",
            ),
            milestone_stats_card(
                stat_name="Completed",
                value=MilestoneState.milestones_by_status["Completed"],
                icon="check-circle",
                icon_color="green",
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
                "repeat(4, 1fr)",
            ],
            width="100%",
            margin_bottom="1em",
        ),
        rx.flex(
            add_milestone_dialog(),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    MilestoneState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=MilestoneState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=MilestoneState.toggle_sort,
                    ),
                ),
                rx.select(
                    ["milestone_name", "target_date", "status", "workstream_id"],
                    placeholder="Sort By: Milestone Name",
                    size="3",
                    on_change=MilestoneState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=MilestoneState.clear_search,
                        display=rx.cond(MilestoneState.search_value, "flex", "none"),
                    ),
                    value=MilestoneState.search_value,
                    placeholder="Search milestones...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=MilestoneState.set_search_value,
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
                        _header_cell("Milestone Name", "flag"),
                        _header_cell("Target Date", "calendar"),
                        _header_cell("Status", "activity"),
                        _header_cell("Workstream ID", "layers"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        MilestoneState.current_page_milestones,
                        lambda milestone, index: show_milestone(milestone, index),
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