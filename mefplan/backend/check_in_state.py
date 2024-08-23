import reflex as rx
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional, Literal

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

CheckInTypeEnum = Literal["Weekly", "Bi-weekly", "Monthly", "End-of-month"]
CheckInStatusEnum = Literal["Not Started", "In Progress", "Completed"]


class CheckInBase(rx.Base):
    check_in_id: Optional[int] = None
    check_in_type: CheckInTypeEnum
    date: str
    notes: Optional[str] = None
    participants: List[int] = []
    status: CheckInStatusEnum = "Not Started"


class CheckInState(rx.State):
    check_ins: List[CheckInBase] = []
    page_number: int = 1
    items_per_page: int = 10
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False
    new_check_in_type: CheckInTypeEnum = "Weekly"
    new_check_in_date: str = ""
    new_check_in_notes: str = ""
    new_check_in_status: CheckInStatusEnum = "Not Started"
    check_in_modal_open: bool = False

    def get_check_in_info(self):
        try:
            response = supabase.table("check_ins").select("*").execute()
            if response.data:
                self.check_ins = [CheckInBase(**item) for item in response.data]
            else:
                print("No data found in the table.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def add_check_in_to_db(self, form_data: dict):
        new_check_in = CheckInBase(
            check_in_type=form_data["check_in_type"],
            date=form_data["date"],
            notes=form_data["notes"],
            status=form_data["status"],
        )
        try:
            response = supabase.table("check_ins").insert(new_check_in.dict()).execute()
            if response.data:
                self.check_ins.append(new_check_in)
                self.get_check_in_info()  # Refresh the check-ins from the database
            else:
                print("Failed to add new check-in.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def handle_submit(self, form_data: dict):
        self.add_check_in_to_db(form_data)
        self.close_check_in_modal()

    @rx.var
    def total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_check_ins) + self.items_per_page - 1)
            // self.items_per_page,
        )

    @rx.var
    def filtered_check_ins(self) -> List[CheckInBase]:
        if not self.search_value:
            return self.check_ins
        search_value = self.search_value.lower()
        return [
            c
            for c in self.check_ins
            if search_value in c.date.lower()
            or search_value in c.check_in_type.lower()
            or search_value in c.status.lower()
            or (c.notes and search_value in c.notes.lower())
        ]

    @rx.var
    def sorted_check_ins(self) -> List[CheckInBase]:
        if not self.sort_value:
            return self.filtered_check_ins
        return sorted(
            self.filtered_check_ins,
            key=lambda c: getattr(c, self.sort_value),
            reverse=self.sort_reverse,
        )

    @rx.var
    def current_page_check_ins(self) -> List[CheckInBase]:
        start = (self.page_number - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_check_ins[start:end]

    @rx.var
    def total_check_ins(self) -> int:
        return len(self.check_ins)

    @rx.var
    def check_ins_by_type(self) -> dict:
        return {
            check_in_type: len(
                [c for c in self.check_ins if c.check_in_type == check_in_type]
            )
            for check_in_type in CheckInTypeEnum.__args__
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
        if isinstance(value, dict):
            value = value.get("value", "")
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

    def open_check_in_modal(self):
        self.check_in_modal_open = True

    def close_check_in_modal(self):
        self.check_in_modal_open = False

    def set_new_check_in_type(self, value: CheckInTypeEnum):
        self.new_check_in_type = value

    def set_new_check_in_date(self, value: str):
        self.new_check_in_date = value

    def set_new_check_in_notes(self, value: str):
        self.new_check_in_notes = value

    def set_new_check_in_status(self, value: CheckInStatusEnum):
        self.new_check_in_status = value

    def get_check_ins_by_type(
        self, check_in_type: CheckInTypeEnum
    ) -> List[CheckInBase]:
        return [c for c in self.check_ins if c.check_in_type == check_in_type]
