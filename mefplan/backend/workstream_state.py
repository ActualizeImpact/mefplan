import reflex as rx
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional, Literal

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

WorkstreamCategoryVar = Literal[
    "Organizational Capacity",
    "Charter School Support and Advocacy",
    "Data Management and Reporting",
    "Financial Stability",
    "Strategic Initiatives",
]


class WorkstreamBase(rx.Base):
    workstream_id: Optional[int] = None
    workstream_name: str
    description: Optional[str] = None
    category: WorkstreamCategoryVar


class WorkstreamState(rx.State):
    workstreams: List[WorkstreamBase] = []
    page_number: int = 1
    items_per_page: int = 10
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False
    new_workstream_name: str = ""
    new_description: str = ""
    new_category: WorkstreamCategoryVar = "Organizational Capacity"
    workstream_modal_open: bool = False

    def get_workstream_info(self):
        try:
            response = supabase.table("workstreams").select("*").execute()
            if response.data:
                self.workstreams = [WorkstreamBase(**item) for item in response.data]
            else:
                print("No data found in the table.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def add_workstream_to_db(self, form_data: dict):
        new_workstream = WorkstreamBase(
            workstream_name=form_data["workstream_name"],
            description=form_data.get("description"),
            category=form_data["category"],
        )
        try:
            response = (
                supabase.table("workstreams").insert(new_workstream.dict()).execute()
            )
            if response.data:
                self.workstreams.append(new_workstream)
                self.get_workstream_info()  # Refresh the workstreams from the database
            else:
                print("Failed to add new workstream.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def handle_submit(self, form_data: dict):
        self.add_workstream_to_db(form_data)
        self.close_workstream_modal()

    @rx.var
    def total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_workstreams) + self.items_per_page - 1)
            // self.items_per_page,
        )

    @rx.var
    def filtered_workstreams(self) -> List[WorkstreamBase]:
        if not self.search_value:
            return self.workstreams
        search_value = self.search_value.lower()
        return [
            w
            for w in self.workstreams
            if search_value in w.workstream_name.lower()
            or (w.description and search_value in w.description.lower())
            or search_value in w.category.lower()
        ]

    @rx.var
    def sorted_workstreams(self) -> List[WorkstreamBase]:
        if not self.sort_value:
            return self.filtered_workstreams
        return sorted(
            self.filtered_workstreams,
            key=lambda w: getattr(w, self.sort_value),
            reverse=self.sort_reverse,
        )

    @rx.var
    def current_page_workstreams(self) -> List[WorkstreamBase]:
        start = (self.page_number - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_workstreams[start:end]

    @rx.var
    def total_workstreams(self) -> int:
        return len(self.workstreams)

    @rx.var
    def workstreams_by_category(self) -> dict:
        return {
            category: len([w for w in self.workstreams if w.category == category])
            for category in WorkstreamCategoryVar.__args__
        }

    def next_page(self):
        if self.page_number < self.total_pages:
            self.page_number += 1

    def prev_page(self):
        if self.page_number > 1:
            self.page_number -= 1

    def first_page(self):
        self.page_number = 1

    def last_page(self):
        self.page_number = self.total_pages

    def set_search_value(self, value: str):
        self.search_value = value
        self.page_number = 1

    def clear_search(self):
        self.set_search_value("")

    def set_sort_value(self, value: str):
        if self.sort_value == value:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_value = value
            self.sort_reverse = False
        self.page_number = 1

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse

    def open_workstream_modal(self):
        self.workstream_modal_open = True

    def close_workstream_modal(self):
        self.workstream_modal_open = False

    def set_new_workstream_name(self, value: str):
        self.new_workstream_name = value

    def set_new_description(self, value: str):
        self.new_description = value

    def set_new_category(self, value: WorkstreamCategoryVar):
        self.new_category = value

    def get_workstreams_by_category(
        self, category: WorkstreamCategoryVar
    ) -> List[WorkstreamBase]:
        return [w for w in self.workstreams if w.category == category]
