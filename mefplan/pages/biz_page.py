import reflex as rx
from ..backend.biz_state import BizState, Business, IndustryEnum
from ..templates import template
from ..components.biz_stats_card import biz_stats_card


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


def show_business(business: Business, index: int) -> rx.Component:
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
        rx.table.row_header_cell(business.company_name),
        rx.table.cell(business.website),
        rx.table.cell(business.industry),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(BizState.page_number),
            f" of {BizState.total_pages}",
        ),
        rx.spacer(),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=16),
                on_click=BizState.first_page,
                opacity=rx.cond(BizState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(BizState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=16),
                on_click=BizState.prev_page,
                opacity=rx.cond(BizState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(BizState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=16),
                on_click=BizState.next_page,
                opacity=rx.cond(BizState.page_number == BizState.total_pages, 0.6, 1),
                color_scheme=rx.cond(
                    BizState.page_number == BizState.total_pages, "gray", "accent"
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=16),
                on_click=BizState.last_page,
                opacity=rx.cond(BizState.page_number == BizState.total_pages, 0.6, 1),
                color_scheme=rx.cond(
                    BizState.page_number == BizState.total_pages, "gray", "accent"
                ),
                variant="soft",
            ),
            spacing="1",
        ),
        width="100%",
        padding_top="0.5em",
    )


def add_business_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Business", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="building", size=34),
                    color_scheme="blue",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Business",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the business info",
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
                            rx.form.label("Company Name"),
                            rx.input(
                                placeholder="Enter company name", name="company_name"
                            ),
                        ),
                        rx.form.field(
                            rx.form.label("Website"),
                            rx.input(placeholder="Enter website URL", name="website"),
                        ),
                        rx.form.field(
                            rx.form.label("Industry"),
                            rx.select(
                                list(IndustryEnum.__args__),
                                placeholder="Select industry",
                                name="industry",
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
                                rx.button("Add Business"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=BizState.add_business_to_db,
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
    route="/blackbiz",
    title="Black Business Finder",
    on_load=BizState.get_business_info(),
    hidden_routes=["/admin", "/signup", "/login"],
)
def biz_page():
    return rx.vstack(
        rx.heading("Business Information", margin_bottom="1em"),
        rx.grid(
            biz_stats_card(
                stat_name="Total Businesses",
                value=BizState.total_businesses,
                icon="building",
                icon_color="blue",
            ),
            biz_stats_card(
                stat_name="Industries",
                value=BizState.total_industries,
                icon="briefcase",
                icon_color="pink",
            ),
            biz_stats_card(
                stat_name="Businesses with Website",
                value=BizState.businesses_with_website,
                icon="link",
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
            add_business_dialog(),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    BizState.sort_reverse,
                    rx.icon(
                        "arrow-down-z-a",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=BizState.toggle_sort,
                    ),
                    rx.icon(
                        "arrow-down-a-z",
                        size=28,
                        stroke_width=1.5,
                        cursor="pointer",
                        flex_shrink="0",
                        on_click=BizState.toggle_sort,
                    ),
                ),
                rx.select(
                    ["company_name", "website", "industry"],
                    placeholder="Sort By: Company Name",
                    size="3",
                    on_change=BizState.set_sort_value,
                ),
                rx.input(
                    rx.input.slot(rx.icon("search")),
                    rx.input.slot(
                        rx.icon("x"),
                        justify="end",
                        cursor="pointer",
                        on_click=BizState.set_search_value(""),
                        display=rx.cond(BizState.search_value, "flex", "none"),
                    ),
                    value=BizState.search_value,
                    placeholder="Search here...",
                    size="3",
                    max_width=["150px", "150px", "200px", "250px"],
                    width="100%",
                    variant="surface",
                    color_scheme="gray",
                    on_change=BizState.set_search_value,
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
                        _header_cell("Company Name", "building"),
                        _header_cell("Website", "link"),
                        _header_cell("Industry", "briefcase"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        BizState.current_page_businesses,
                        lambda business, index: show_business(business, index),
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
