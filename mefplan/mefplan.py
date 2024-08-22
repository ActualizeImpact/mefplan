# mefplan.py
import reflex as rx
from state.app_state import AppState
from components.dashboard import dashboard
from components.workstream_management import workstream_management
from components.task_management import task_management
from components.milestone_tracker import milestone_tracker
from components.staff_management import staff_management
from components.reporting import reporting
from components.meeting_management import meeting_management
from components.objectives_tracking import objectives_tracking
from components.check_in_system import check_in_system

def index() -> rx.Component:
    return rx.theme(
        rx.container(
            rx.vstack(
                rx.heading("MEF 90-Day Plan", size="lg"),
                rx.tabs.root(
                    rx.tabs.list(
                        rx.tabs.trigger("Dashboard"),
                        rx.tabs.trigger("Workstreams"),
                        rx.tabs.trigger("Tasks"),
                        rx.tabs.trigger("Milestones"),
                        rx.tabs.trigger("Staff"),
                        rx.tabs.trigger("Reports"),
                        rx.tabs.trigger("Meetings"),
                        rx.tabs.trigger("Objectives"),
                        rx.tabs.trigger("Check-Ins"),
                    ),
                    rx.tabs.content("Dashboard", dashboard()),
                    rx.tabs.content("Workstreams", workstream_management()),
                    rx.tabs.content("Tasks", task_management()),
                    rx.tabs.content("Milestones", milestone_tracker()),
                    rx.tabs.content("Staff", staff_management()),
                    rx.tabs.content("Reports", reporting()),
                    rx.tabs.content("Meetings", meeting_management()),
                    rx.tabs.content("Objectives", objectives_tracking()),
                    rx.tabs.content("Check-Ins", check_in_system()),
                ),
                width="100%",
                spacing="4",
            ),
            max_width="1200px",
            padding="4",
        )
    )

app = rx.App(state=AppState)
app.add_page(index)