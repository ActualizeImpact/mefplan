import reflex as rx
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional, Literal

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class StaffMemberBase(rx.Base):
    staff_member_id: Optional[int] = None
    first_name: str
    last_name: str
    role: str
    email: str
    phone: Optional[str] = None
    assigned_workstream_ids: list[int]


class StaffManagementState(rx.State):
    staff_members: List[StaffMemberBase] = []
    page_number: int = 1
    items_per_page: int = 10
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False
    new_first_name: str = ""
    new_last_name: str = ""
    new_role: str = ""
    new_email: str = ""
    new_phone: str = ""
    new_assigned_workstream_ids: list[int] = []
    staff_modal_open: bool = False

    def get_staff_info(self):
        try:
            response = supabase.table("staff_members").select("*").execute()
            if response.data:
                self.staff_members = [StaffMemberBase(**item) for item in response.data]
            else:
                print("No data found in the table.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def add_staff_member_to_db(self, form_data: dict):
        new_staff_member = StaffMemberBase(
            first_name=form_data["first_name"],
            last_name=form_data["last_name"],
            role=form_data["role"],
            email=form_data["email"],
            phone=form_data.get("phone"),
            assigned_workstream_ids=form_data["assigned_workstream_ids"],
        )
        try:
            response = (
                supabase.table("staff_members")
                .insert(new_staff_member.dict())
                .execute()
            )
            if response.data:
                self.staff_members.append(new_staff_member)
                self.get_staff_info()  # Refresh the staff members from the database
            else:
                print("Failed to add new staff member.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def handle_submit(self, form_data: dict):
        self.add_staff_member_to_db(form_data)
        self.close_staff_modal()

    @rx.var
    def total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_staff_members) + self.items_per_page - 1)
            // self.items_per_page,
        )

    @rx.var
    def filtered_staff_members(self) -> List[StaffMemberBase]:
        if not self.search_value:
            return self.staff_members
        search_value = self.search_value.lower()
        return [
            s
            for s in self.staff_members
            if search_value in s.first_name.lower()
            or search_value in s.last_name.lower()
            or search_value in s.role.lower()
            or search_value in s.email.lower()
            or (s.phone and search_value in s.phone.lower())
        ]

    @rx.var
    def sorted_staff_members(self) -> List[StaffMemberBase]:
        if not self.sort_value:
            return self.filtered_staff_members
        return sorted(
            self.filtered_staff_members,
            key=lambda s: getattr(s, self.sort_value),
            reverse=self.sort_reverse,
        )

    @rx.var
    def current_page_staff_members(self) -> List[StaffMemberBase]:
        start = (self.page_number - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_staff_members[start:end]

    @rx.var
    def total_staff_members(self) -> int:
        return len(self.staff_members)

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

    def open_staff_modal(self):
        self.staff_modal_open = True

    def close_staff_modal(self):
        self.staff_modal_open = False

    def set_new_first_name(self, value: str):
        self.new_first_name = value

    def set_new_last_name(self, value: str):
        self.new_last_name = value

    def set_new_role(self, value: str):
        self.new_role = value

    def set_new_email(self, value: str):
        self.new_email = value

    def set_new_phone(self, value: str):
        self.new_phone = value

    def set_new_assigned_workstream_ids(self, value: list[int]):
        self.new_assigned_workstream_ids = value

    def get_staff_members_by_role(self, role: str) -> List[StaffMemberBase]:
        return [s for s in self.staff_members if s.role == role]
