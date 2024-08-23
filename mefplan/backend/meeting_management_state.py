import reflex as rx
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime, date

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class Meeting(rx.Base):
    meeting_id: Optional[int] = None
    meeting_title: str
    meeting_date: str
    meeting_notes: Optional[str] = None
    participants: Optional[str] = None
    workstream_id: int


class MeetingState(rx.State):
    meetings: List[Meeting] = []
    staff_members: List[str] = []  # This should be populated with actual staff members
    page_number: int = 1
    items_per_page: int = 10
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False
    meeting_modal_open: bool = False

    def get_meeting_info(self):
        try:
            response = supabase.table("meetings").select("*").execute()
            if response.data:
                self.meetings = [Meeting(**item) for item in response.data]
            else:
                print("No data found in the table.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def add_meeting(self, form_data: dict):
        new_meeting = Meeting(
            meeting_title=form_data["meeting_title"],
            meeting_date=form_data["meeting_date"],
            meeting_notes=form_data.get("meeting_notes", ""),
            participants=form_data.get("participants", ""),
            workstream_id=form_data["workstream_id"],
        )
        try:
            response = supabase.table("meetings").insert(new_meeting.dict()).execute()
            if response.data:
                self.meetings.append(new_meeting)
                self.get_meeting_info()  # Refresh the meetings from the database
            else:
                print("Failed to add new meeting.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        self.close_meeting_modal()

    def handle_submit(self, form_data: dict):
        self.add_meeting(form_data)

    @rx.var
    def total_meetings(self) -> int:
        return len(self.meetings)

    @rx.var
    def upcoming_meetings(self) -> int:
        today = date.today()
        return sum(
            1
            for meeting in self.meetings
            if datetime.strptime(meeting.meeting_date, "%Y-%m-%d").date() >= today
        )

    @rx.var
    def past_meetings(self) -> int:
        today = date.today()
        return sum(
            1
            for meeting in self.meetings
            if datetime.strptime(meeting.meeting_date, "%Y-%m-%d").date() < today
        )

    @rx.var
    def total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_meetings) + self.items_per_page - 1)
            // self.items_per_page,
        )

    @rx.var
    def filtered_meetings(self) -> List[Meeting]:
        if not self.search_value:
            return self.meetings
        search_value = self.search_value.lower()
        return [
            m
            for m in self.meetings
            if search_value in m.meeting_title.lower()
            or search_value in m.meeting_date.lower()
            or (m.participants and search_value in m.participants.lower())
            or (m.meeting_notes and search_value in m.meeting_notes.lower())
        ]

    @rx.var
    def sorted_meetings(self) -> List[Meeting]:
        if not self.sort_value:
            return self.filtered_meetings
        return sorted(
            self.filtered_meetings,
            key=lambda m: getattr(m, self.sort_value),
            reverse=self.sort_reverse,
        )

    @rx.var
    def current_page_meetings(self) -> List[Meeting]:
        start = (self.page_number - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_meetings[start:end]

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

    def open_meeting_modal(self):
        self.meeting_modal_open = True

    def close_meeting_modal(self):
        self.meeting_modal_open = False
