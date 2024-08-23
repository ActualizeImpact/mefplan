import reflex as rx
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import List, Optional, Literal

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TaskStatusVar = Literal["Not Started", "In Progress", "Completed", "On Hold"]
TaskPriorityVar = Literal["Low", "Medium", "High", "Urgent"]


class TaskBase(rx.Base):
    task_id: Optional[int] = None
    task_name: str
    description: Optional[str] = None
    start_date: str
    end_date: str
    status: TaskStatusVar
    priority: TaskPriorityVar
    workstream_id: int
    assigned_to: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class TaskManagementState(rx.State):
    tasks: List[TaskBase] = []
    page_number: int = 1
    items_per_page: int = 10
    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False
    new_task_name: str = ""
    new_description: str = ""
    new_start_date: str = ""
    new_end_date: str = ""
    new_status: TaskStatusVar = "Not Started"
    new_priority: TaskPriorityVar = "Medium"
    new_workstream_id: int = 0
    new_assigned_to: int = 0
    task_modal_open: bool = False

    def get_task_info(self):
        try:
            response = supabase.table("tasks").select("*").execute()
            if response.data:
                self.tasks = [TaskBase(**item) for item in response.data]
            else:
                print("No data found in the table.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def add_task_to_db(self, form_data: dict):
        new_task = TaskBase(
            task_name=form_data["task_name"],
            description=form_data.get("description"),
            start_date=form_data["start_date"],
            end_date=form_data["end_date"],
            status=form_data["status"],
            priority=form_data["priority"],
            workstream_id=form_data["workstream_id"],
            assigned_to=form_data["assigned_to"],
        )
        try:
            response = supabase.table("tasks").insert(new_task.dict()).execute()
            if response.data:
                self.tasks.append(new_task)
                self.get_task_info()  # Refresh the tasks from the database
            else:
                print("Failed to add new task.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def handle_submit(self, form_data: dict):
        self.add_task_to_db(form_data)
        self.close_task_modal()

    @rx.var
    def total_pages(self) -> int:
        return max(
            1,
            (len(self.filtered_tasks) + self.items_per_page - 1) // self.items_per_page,
        )

    @rx.var
    def filtered_tasks(self) -> List[TaskBase]:
        if not self.search_value:
            return self.tasks
        search_value = self.search_value.lower()
        return [
            t
            for t in self.tasks
            if search_value in t.task_name.lower()
            or (t.description and search_value in t.description.lower())
            or search_value in t.status.lower()
            or search_value in t.priority.lower()
        ]

    @rx.var
    def sorted_tasks(self) -> List[TaskBase]:
        if not self.sort_value:
            return self.filtered_tasks
        return sorted(
            self.filtered_tasks,
            key=lambda t: getattr(t, self.sort_value),
            reverse=self.sort_reverse,
        )

    @rx.var
    def current_page_tasks(self) -> List[TaskBase]:
        start = (self.page_number - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_tasks[start:end]

    @rx.var
    def total_tasks(self) -> int:
        return len(self.tasks)

    @rx.var
    def tasks_by_status(self) -> dict:
        return {
            status: len([t for t in self.tasks if t.status == status])
            for status in TaskStatusVar.__args__
        }

    @rx.var
    def tasks_by_priority(self) -> dict:
        return {
            priority: len([t for t in self.tasks if t.priority == priority])
            for priority in TaskPriorityVar.__args__
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

    def open_task_modal(self):
        self.task_modal_open = True

    def close_task_modal(self):
        self.task_modal_open = False

    def set_new_task_name(self, value: str):
        self.new_task_name = value

    def set_new_description(self, value: str):
        self.new_description = value

    def set_new_start_date(self, value: str):
        self.new_start_date = value

    def set_new_end_date(self, value: str):
        self.new_end_date = value

    def set_new_status(self, value: TaskStatusVar):
        self.new_status = value

    def set_new_priority(self, value: TaskPriorityVar):
        self.new_priority = value

    def set_new_workstream_id(self, value: int):
        self.new_workstream_id = value

    def set_new_assigned_to(self, value: int):
        self.new_assigned_to = value

    def get_tasks_by_status(self, status: TaskStatusVar) -> List[TaskBase]:
        return [t for t in self.tasks if t.status == status]

    def get_tasks_by_priority(self, priority: TaskPriorityVar) -> List[TaskBase]:
        return [t for t in self.tasks if t.priority == priority]

    def get_tasks_by_workstream(self, workstream_id: int) -> List[TaskBase]:
        return [t for t in self.tasks if t.workstream_id == workstream_id]

    def get_tasks_by_assigned_to(self, assigned_to: int) -> List[TaskBase]:
        return [t for t in self.tasks if t.assigned_to == assigned_to]
