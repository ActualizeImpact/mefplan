import reflex as rx
from ..backend.task_management_state import (
    TaskManagementState,
    TaskBase,
    TaskStatusVar,
    TaskPriorityVar,
)
from ..templates import template
from ..components.task_stats_card import task_stats_card


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def show_task(task: TaskBase, index: int) -> rx.Component:
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
        rx.table.row_header_cell(task.task_name),
        rx.table.cell(task.status),
        rx.table.cell(task.priority),
        rx.table.cell(task.start_date),
        rx.table.cell(task.end_date),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(TaskManagementState.page_number),
            f" of {TaskManagementState.total_pages}",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=16),
                on_click=TaskManagementState.first_page,
                opacity=rx.cond(TaskManagementState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(
                    TaskManagementState.page_number == 1, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=16),
                on_click=TaskManagementState.prev_page,
                opacity=rx.cond(TaskManagementState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(
                    TaskManagementState.page_number == 1, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=16),
                on_click=TaskManagementState.next_page,
                opacity=rx.cond(
                    TaskManagementState.page_number == TaskManagementState.total_pages,
                    0.6,
                    1,
                ),
                color_scheme=rx.cond(
                    TaskManagementState.page_number == TaskManagementState.total_pages,
                    "gray",
                    "accent",
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=16),
                on_click=TaskManagementState.last_page,
                opacity=rx.cond(
                    TaskManagementState.page_number == TaskManagementState.total_pages,
                    0.6,
                    1,
                ),
                color_scheme=rx.cond(
                    TaskManagementState.page_number == TaskManagementState.total_pages,
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


def add_task_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Task", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="clipboard", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Task",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the task info",
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
                            rx.form.label("Task Name"),
                            rx.input(placeholder="Enter task name", name="task_name"),
                        ),
                        rx.form.field(
                            rx.form.label("Description"),
                            rx.text_area(
                                placeholder="Enter task description", name="description"
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Start Date"),
                            rx.input(type_="date", name="start_date"),
                        ),
                        rx.form.field(
                            rx.form.label("End Date"),
                            rx.input(type_="date", name="end_date"),
                        ),
                        rx.form.field(
                            rx.form.label("Status"),
                            rx.select(
                                list(TaskStatusVar.__args__),
                                placeholder="Select status",
                                name="status",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Priority"),
                            rx.select(
                                list(TaskPriorityVar.__args__),
                                placeholder="Select priority",
                                name="priority",
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Workstream ID"),
                            rx.input(
                                placeholder="Enter workstream ID", name="workstream_id"
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Assigned To"),
                            rx.input(placeholder="Enter user ID", name="assigned_to"),
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
                                rx.button("Add Task"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=TaskManagementState.handle_submit,
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
    route="/tasks",
    title="Task Management",
    on_load=TaskManagementState.get_task_info(),
)
def task_management_page():
    return rx.vstack(
        rx.heading("Task Management", margin_bottom="1em"),
        rx.grid(
            task_stats_card(
                stat_name="Total Tasks",
                value=TaskManagementState.total_tasks,
                icon="clipboard",
                icon_color="blue",
            ),
            task_stats_card(
                stat_name="Not Started",
                value=TaskManagementState.tasks_by_status["Not Started"],
                icon="circle",
                icon_color="red",
            ),
            task_stats_card(
                stat_name="In Progress",
                value=TaskManagementState.tasks_by_status["In Progress"],
                icon="clock",
                icon_color="yellow",
            ),
            task_stats_card(
                stat_name="Completed",
                value=TaskManagementState.tasks_by_status["Completed"],
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
            add_task_dialog(),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    TaskManagementState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=TaskManagementState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=TaskManagementState.toggle_sort,
                    ),
                ),
                rx.select(
                    ["task_name", "status", "priority", "start_date", "end_date"],
                    placeholder="Sort By: Task Name",
                    size="3",
                    on_change=TaskManagementState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=TaskManagementState.clear_search,
                        display=rx.cond(
                            TaskManagementState.search_value, "flex", "none"
                        ),
                    ),
                    value=TaskManagementState.search_value,
                    placeholder="Search tasks...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=TaskManagementState.set_search_value,
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
                        _header_cell("Task Name", "clipboard"),
                        _header_cell("Status", "activity"),
                        _header_cell("Priority", "alert-triangle"),
                        _header_cell("Start Date", "calendar"),
                        _header_cell("End Date", "calendar"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        TaskManagementState.current_page_tasks,
                        lambda task, index: show_task(task, index),
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
