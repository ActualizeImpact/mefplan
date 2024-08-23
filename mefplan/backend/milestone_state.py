import reflex as rx
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional, Literal

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

MilestoneStatusVar = Literal["Not Started", "In Progress", "Completed", "Delayed"]


class MilestoneBase(rx.Base):
    milestone_id: Optional[int] = None
    milestone_name: str
    target_date: str
    status: MilestoneStatusVar
    workstream_id: int
    objective_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class MilestoneState(rx.State):
    milestones: List[MilestoneBase] = []
    page_number: int = 1
    items_per_page: int = 10
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False
    new_milestone_name: str = ""
    new_target_date: str = ""
    new_status: MilestoneStatusVar = "Not Started"
    new_workstream_id: int = 0
    new_objective_id: Optional[int] = None
    milestone_modal_open: bool = False

    def get_milestone_info(self):
        try:
            response = supabase.table("milestones").select("*").execute()
            if response.data:
                self.milestones = [MilestoneBase(**item) for item in response.data]
            else:
                print("No data found in the table.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def add_milestone_to_db(self, form_data: dict):
        new_milestone = MilestoneBase(
            milestone_name=form_data["milestone_name"],
            target_date=form_data["target_date"],
            status=form_data["status"],
            workstream_id=form_data["workstream_id"],
            objective_id=form_data.get("objective_id"),
        )
        try:
            response = (
                supabase.table("milestones").insert(new_milestone.dict()).execute()
            )
            if response.data:
                self.milestones.append(new_milestone)
                self.get_milestone_info()  # Refresh the milestones from the database
            else:
                print("Failed to add new milestone.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def handle_submit(self, form_data: dict):
        self.add_milestone_to_db(form_data)
        self.close_milestone_modal()

    @rx.var
    def total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_milestones) + self.items_per_page - 1)
            // self.items_per_page,
        )

    @rx.var
    def filtered_milestones(self) -> List[MilestoneBase]:
        if not self.search_value:
            return self.milestones
        search_value = self.search_value.lower()
        return [
            m
            for m in self.milestones
            if search_value in m.milestone_name.lower()
            or search_value in m.target_date.lower()
            or search_value in m.status.lower()
        ]

    @rx.var
    def sorted_milestones(self) -> List[MilestoneBase]:
        if not self.sort_value:
            return self.filtered_milestones
        return sorted(
            self.filtered_milestones,
            key=lambda m: getattr(m, self.sort_value),
            reverse=self.sort_reverse,
        )

    @rx.var
    def current_page_milestones(self) -> List[MilestoneBase]:
        start = (self.page_number - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_milestones[start:end]

    @rx.var
    def total_milestones(self) -> int:
        return len(self.milestones)

    @rx.var
    def milestones_by_status(self) -> dict:
        return {
            status: len([m for m in self.milestones if m.status == status])
            for status in MilestoneStatusVar.__args__
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

    def open_milestone_modal(self):
        self.milestone_modal_open = True

    def close_milestone_modal(self):
        self.milestone_modal_open = False

    def set_new_milestone_name(self, value: str):
        self.new_milestone_name = value

    def set_new_target_date(self, value: str):
        self.new_target_date = value

    def set_new_status(self, value: MilestoneStatusVar):
        self.new_status = value

    def set_new_workstream_id(self, value: int):
        self.new_workstream_id = value

    def set_new_objective_id(self, value: Optional[int]):
        self.new_objective_id = value

    def get_milestones_by_status(
        self, status: MilestoneStatusVar
    ) -> List[MilestoneBase]:
        return [m for m in self.milestones if m.status == status]
