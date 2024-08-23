import reflex as rx
from ..state.app_state import AppState
from ..utils.constants import REPORT_TYPES


def reporting() -> rx.Component:
    return rx.vstack(
        rx.heading("Reporting", size="md"),
        rx.select(
            REPORT_TYPES,
            placeholder="Select Report Type",
            on_change=AppState.set_selected_report_type,
        ),
        rx.button("Generate Report", on_click=AppState.generate_report),
        rx.cond(
            AppState.report_data,
            rx.vstack(
                rx.heading("Report Results", size="sm"),
                rx.data_table(
                    data=AppState.report_data,
                    columns=AppState.report_columns,
                ),
            ),
        ),
        width="100%",
    )
