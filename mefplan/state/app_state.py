import reflex as rx
from typing import List, Dict, Any, Literal, Optional
from data.crud_operations import (
    get_all_tasks,
    get_all_workstreams,
    get_all_staff_members,
    get_all_milestones,
    get_all_objectives,
    get_all_check_ins,
)

# Enum types
TaskStatusVar = Literal["Not Started", "In Progress", "Completed", "On Hold"]
TaskPriorityVar = Literal["Low", "Medium", "High", "Urgent"]
MilestoneStatusVar = Literal["Not Started", "In Progress", "Completed", "Delayed"]
WorkstreamCategoryVar = Literal[
    "Organizational Capacity",
    "Charter School Support and Advocacy",
    "Data Management and Reporting",
    "Financial Stability",
    "Strategic Initiatives",
]


# Base classes
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


class WorkstreamBase(rx.Base):
    workstream_id: Optional[int] = None
    workstream_name: str
    description: Optional[str] = None
    category: WorkstreamCategoryVar


class StaffMemberBase(rx.Base):
    staff_member_id: Optional[int] = None
    first_name: str
    last_name: str
    role: str
    email: str
    phone: Optional[str] = None
    assigned_workstream_ids: list[int]


class MilestoneBase(rx.Base):
    milestone_id: Optional[int] = None
    milestone_name: str
    target_date: str
    status: MilestoneStatusVar
    workstream_id: int
    objective_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ObjectiveBase(rx.Base):
    objective_id: Optional[int] = None
    objective_name: str
    description: Optional[str] = None
    workstream_id: int
    target_date: str
    status: MilestoneStatusVar


class CheckInBase(rx.Base):
    check_in_id: Optional[int] = None
    check_in_type: Literal["Weekly", "Bi-weekly", "Monthly", "End-of-month"]
    date: str
    notes: Optional[str] = None
    participants: list[int]  # List of staff_member_ids


class AppState(rx.State):
    tasks: List[TaskBase] = []
    workstreams: List[WorkstreamBase] = []
    staff_members: List[StaffMemberBase] = []
    milestones: List[MilestoneBase] = []
    objectives: List[ObjectiveBase] = []
    check_ins: List[CheckInBase] = []

    workstream_modal_open: bool = False
    task_modal_open: bool = False

    new_workstream_name: str = ""
    new_workstream_category: str = ""
    new_workstream_description: str = ""

    new_task_name: str = ""
    new_task_status: str = ""
    new_task_priority: str = ""
    new_task_start_date: str = ""
    new_task_end_date: str = ""
    new_task_assigned_to: int = 0

    # New variables for check-ins
    weekly_check_ins: List[CheckInBase] = []
    biweekly_check_ins: List[CheckInBase] = []
    monthly_check_ins: List[CheckInBase] = []
    end_of_month_check_ins: List[CheckInBase] = []
    check_in_modal_open: bool = False
    new_check_in_date: str = ""
    new_check_in_notes: str = ""
    new_check_in_type: str = ""

    def init(self):
        self.tasks = get_all_tasks()
        self.workstreams = get_all_workstreams()
        self.staff_members = get_all_staff_members()
        self.milestones = get_all_milestones()
        self.objectives = get_all_objectives()
        self.check_ins = get_all_check_ins()
        self.weekly_check_ins = [
            check_in
            for check_in in self.check_ins
            if check_in.check_in_type == "Weekly"
        ]
        self.biweekly_check_ins = [
            check_in
            for check_in in self.check_ins
            if check_in.check_in_type == "Bi-weekly"
        ]
        self.monthly_check_ins = [
            check_in
            for check_in in self.check_ins
            if check_in.check_in_type == "Monthly"
        ]
        self.end_of_month_check_ins = [
            check_in
            for check_in in self.check_ins
            if check_in.check_in_type == "End-of-month"
        ]

    @rx.var
    def total_tasks(self) -> int:
        return len(self.tasks)

    @rx.var
    def tasks_by_status(self) -> List[Dict[str, Any]]:
        status_counts = {}
        for task in self.tasks:
            status_counts[task.status] = status_counts.get(task.status, 0) + 1
        return [
            {"name": status, "value": count} for status, count in status_counts.items()
        ]

    @rx.var
    def upcoming_milestones(self) -> List[MilestoneBase]:
        return sorted(self.milestones, key=lambda m: m.target_date)[:5]

    @rx.var
    def recent_activity(self) -> List[str]:
        # This is a placeholder. In a real application, you'd implement logic to track recent activities.
        return ["Task 1 completed", "New milestone added", "Workstream 2 updated"]

    @rx.var
    def workstream_categories(self) -> List[str]:
        return [
            "Organizational Capacity",
            "Charter School Support and Advocacy",
            "Data Management and Reporting",
            "Financial Stability",
            "Strategic Initiatives",
        ]

    @rx.var
    def task_statuses(self) -> List[str]:
        return ["Not Started", "In Progress", "Completed", "On Hold"]

    @rx.var
    def task_priorities(self) -> List[str]:
        return ["Low", "Medium", "High", "Urgent"]

    @rx.var
    def check_in_statuses(self) -> List[str]:
        return ["Not Started", "In Progress", "Completed"]

    def open_workstream_modal(self):
        self.workstream_modal_open = True

    def close_workstream_modal(self):
        self.workstream_modal_open = False

    def set_new_workstream_name(self, name: str):
        self.new_workstream_name = name

    def set_new_workstream_category(self, category: str):
        self.new_workstream_category = category

    def set_new_workstream_description(self, description: str):
        self.new_workstream_description = description

    def add_workstream(self):
        # Add logic to create a new workstream
        new_workstream = WorkstreamBase(
            workstream_name=self.new_workstream_name,
            category=self.new_workstream_category,
            description=self.new_workstream_description,
        )
        self.workstreams.append(new_workstream)
        self.close_workstream_modal()

    def open_task_modal(self):
        self.task_modal_open = True

    def close_task_modal(self):
        self.task_modal_open = False

    def set_new_task_name(self, name: str):
        self.new_task_name = name

    def set_new_task_status(self, status: str):
        self.new_task_status = status

    def set_new_task_priority(self, priority: str):
        self.new_task_priority = priority

    def set_new_task_start_date(self, date: str):
        self.new_task_start_date = date

    def set_new_task_end_date(self, date: str):
        self.new_task_end_date = date

    def set_new_task_assigned_to(self, staff_id: int):
        self.new_task_assigned_to = staff_id

    def add_task(self):
        # Add logic to create a new task
        new_task = TaskBase(
            task_name=self.new_task_name,
            status=self.new_task_status,
            priority=self.new_task_priority,
            start_date=self.new_task_start_date,
            end_date=self.new_task_end_date,
            assigned_to=self.new_task_assigned_to,
        )
        self.tasks.append(new_task)
        self.close_task_modal()

    def set_task_modal_open(self, open: bool):
        self.task_modal_open = open

    def open_weekly_check_in_modal(self):
        self.check_in_modal_open = True

    def open_biweekly_check_in_modal(self):
        self.check_in_modal_open = True

    def open_monthly_check_in_modal(self):
        self.check_in_modal_open = True

    def open_end_of_month_check_in_modal(self):
        self.check_in_modal_open = True

    def set_check_in_modal_open(self, open: bool):
        self.check_in_modal_open = open

    def set_new_check_in_date(self, date: str):
        self.new_check_in_date = date

    def set_new_check_in_notes(self, notes: str):
        self.new_check_in_notes = notes

    def set_new_check_in_type(self, check_in_type: str):
        self.new_check_in_type = check_in_type

    def add_check_in(self):
        new_check_in = CheckInBase(
            check_in_type=self.new_check_in_type,
            date=self.new_check_in_date,
            notes=self.new_check_in_notes,
            participants=[],  # You might want to add a way to select participants
        )
        if self.new_check_in_type == "Weekly":
            self.weekly_check_ins.append(new_check_in)
        elif self.new_check_in_type == "Bi-weekly":
            self.biweekly_check_ins.append(new_check_in)
        elif self.new_check_in_type == "Monthly":
            self.monthly_check_ins.append(new_check_in)
        elif self.new_check_in_type == "End-of-month":
            self.end_of_month_check_ins.append(new_check_in)

        self.check_in_modal_open = False
