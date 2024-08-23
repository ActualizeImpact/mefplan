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


class ObjectiveBase(rx.Base):
    objective_id: Optional[int] = None
    objective_name: str
    description: Optional[str] = None
    workstream_id: int
    target_date: str
    status: MilestoneStatusVar


class ObjectiveState(rx.State):
    objectives: List[ObjectiveBase] = []
    page_number: int = 1
    items_per_page: int = 10
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False
    new_objective_name: str = ""
    new_description: str = ""
    new_workstream_id: int = 0
    new_target_date: str = ""
    new_status: MilestoneStatusVar = "Not Started"
    objective_modal_open: bool = False

    def get_objective_info(self):
        try:
            response = supabase.table("objectives").select("*").execute()
            if response.data:
                self.objectives = [ObjectiveBase(**item) for item in response.data]
            else:
                print("No data found in the table.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def add_objective_to_db(self, form_data: dict):
        new_objective = ObjectiveBase(
            objective_name=form_data["objective_name"],
            description=form_data.get("description"),
            workstream_id=form_data["workstream_id"],
            target_date=form_data["target_date"],
            status=form_data["status"],
        )
        try:
            response = (
                supabase.table("objectives").insert(new_objective.dict()).execute()
            )
            if response.data:
                self.objectives.append(new_objective)
                self.get_objective_info()  # Refresh the objectives from the database
            else:
                print("Failed to add new objective.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def handle_submit(self, form_data: dict):
        self.add_objective_to_db(form_data)
        self.close_objective_modal()

    @rx.var
    def total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_objectives) + self.items_per_page - 1)
            // self.items_per_page,
        )

    @rx.var
    def filtered_objectives(self) -> List[ObjectiveBase]:
        if not self.search_value:
            return self.objectives
        search_value = self.search_value.lower()
        return [
            o
            for o in self.objectives
            if search_value in o.objective_name.lower()
            or (o.description and search_value in o.description.lower())
            or search_value in o.target_date.lower()
            or search_value in o.status.lower()
        ]

    @rx.var
    def sorted_objectives(self) -> List[ObjectiveBase]:
        if not self.sort_value:
            return self.filtered_objectives
        return sorted(
            self.filtered_objectives,
            key=lambda o: getattr(o, self.sort_value),
            reverse=self.sort_reverse,
        )

    @rx.var
    def current_page_objectives(self) -> List[ObjectiveBase]:
        start = (self.page_number - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_objectives[start:end]

    @rx.var
    def total_objectives(self) -> int:
        return len(self.objectives)

    @rx.var
    def objectives_by_status(self) -> dict:
        return {
            status: len([o for o in self.objectives if o.status == status])
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

    def open_objective_modal(self):
        self.objective_modal_open = True

    def close_objective_modal(self):
        self.objective_modal_open = False

    def set_new_objective_name(self, value: str):
        self.new_objective_name = value

    def set_new_description(self, value: str):
        self.new_description = value

    def set_new_workstream_id(self, value: int):
        self.new_workstream_id = value

    def set_new_target_date(self, value: str):
        self.new_target_date = value

    def set_new_status(self, value: MilestoneStatusVar):
        self.new_status = value

    def get_objectives_by_status(
        self, status: MilestoneStatusVar
    ) -> List[ObjectiveBase]:
        return [o for o in self.objectives if o.status == status]
