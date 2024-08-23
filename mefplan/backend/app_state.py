import reflex as rx
from typing import List, Dict, Any, Literal, Optional
from ..utils.constants import REPORT_TYPES  # noqa: F401
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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


class MeetingBase(rx.Base):
    meeting_id: Optional[int] = None
    meeting_name: str
    date: str
    time: str
    attendees: List[int]


class AppState(rx.State):
    tasks: List[TaskBase] = []
    workstreams: List[WorkstreamBase] = []
    staff_members: List[StaffMemberBase] = []
    milestones: List[MilestoneBase] = []
    objectives: List[ObjectiveBase] = []
    check_ins: List[CheckInBase] = []
    meetings: List[MeetingBase] = []

    workstream_modal_open: bool = False
    task_modal_open: bool = False
    staff_modal_open: bool = False
    meeting_modal_open: bool = False
    milestone_modal_open: bool = False
    objective_modal_open: bool = False
    check_in_modal_open: bool = False

    new_workstream_name: str = ""
    new_workstream_category: str = ""
    new_workstream_description: str = ""

    new_task_name: str = ""
    new_task_status: str = ""
    new_task_priority: str = ""
    new_task_start_date: str = ""
    new_task_end_date: str = ""
    new_task_assigned_to: int = 0

    new_staff_first_name: str = ""
    new_staff_last_name: str = ""
    new_staff_role: str = ""
    new_staff_email: str = ""
    new_staff_phone: str = ""
    new_staff_workstreams: List[int] = []

    new_meeting_name: str = ""
    new_meeting_date: str = ""
    new_meeting_time: str = ""
    new_meeting_attendees: List[int] = []

    new_milestone_name: str = ""
    new_milestone_target_date: str = ""
    new_milestone_status: MilestoneStatusVar = "Not Started"
    new_milestone_workstream: int = 0

    new_objective_name: str = ""
    new_objective_description: str = ""
    new_objective_workstream: int = 0
    new_objective_target_date: str = ""
    new_objective_status: MilestoneStatusVar = "Not Started"

    new_check_in_date: str = ""
    new_check_in_notes: str = ""
    new_check_in_type: str = ""

    weekly_check_ins: List[CheckInBase] = []
    biweekly_check_ins: List[CheckInBase] = []
    monthly_check_ins: List[CheckInBase] = []
    end_of_month_check_ins: List[CheckInBase] = []

    selected_report_type: str = ""
    report_data: List[Dict[str, Any]] = []
    report_columns: List[Dict[str, str]] = []

    workstream_progress: List[Dict[str, Any]]
    staff_workload: List[Dict[str, Any]]

    def init(self):
        self.tasks = self.get_all_tasks()
        self.workstreams = self.get_all_workstreams()
        self.staff_members = self.get_all_staff_members()
        self.milestones = self.get_all_milestones()
        self.objectives = self.get_all_objectives()
        self.check_ins = self.get_all_check_ins()
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

        self.get_workstream_progress()
        self.get_staff_workload()

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

    def set_staff_modal_open(self, open: bool):
        self.staff_modal_open = open

    def set_new_staff_first_name(self, name: str):
        self.new_staff_first_name = name

    def set_new_staff_last_name(self, name: str):
        self.new_staff_last_name = name

    def set_new_staff_role(self, role: str):
        self.new_staff_role = role

    def set_new_staff_email(self, email: str):
        self.new_staff_email = email

    def set_new_staff_phone(self, phone: str):
        self.new_staff_phone = phone

    def set_new_staff_workstreams(self, workstreams: List[int]):
        self.new_staff_workstreams = workstreams

    def add_staff_member(self):
        new_staff = StaffMemberBase(
            first_name=self.new_staff_first_name,
            last_name=self.new_staff_last_name,
            role=self.new_staff_role,
            email=self.new_staff_email,
            phone=self.new_staff_phone,
            assigned_workstream_ids=self.new_staff_workstreams,
        )
        self.staff_members.append(new_staff)
        self.staff_modal_open = False

    def set_meeting_modal_open(self, open: bool):
        self.meeting_modal_open = open

    def set_new_meeting_name(self, name: str):
        self.new_meeting_name = name

    def set_new_meeting_date(self, date: str):
        self.new_meeting_date = date

    def set_new_meeting_time(self, time: str):
        self.new_meeting_time = time

    def set_new_meeting_attendees(self, attendees: List[int]):
        self.new_meeting_attendees = attendees

    def add_meeting(self):
        new_meeting = MeetingBase(
            meeting_name=self.new_meeting_name,
            date=self.new_meeting_date,
            time=self.new_meeting_time,
            attendees=self.new_meeting_attendees,
        )
        self.meetings.append(new_meeting)
        self.meeting_modal_open = False

    def set_milestone_modal_open(self, open: bool):
        self.milestone_modal_open = open

    def set_new_milestone_name(self, name: str):
        self.new_milestone_name = name

    def set_new_milestone_target_date(self, date: str):
        self.new_milestone_target_date = date

    def set_new_milestone_status(self, status: MilestoneStatusVar):
        self.new_milestone_status = status

    def set_new_milestone_workstream(self, workstream_id: int):
        self.new_milestone_workstream = workstream_id

    def add_milestone(self):
        new_milestone = MilestoneBase(
            milestone_name=self.new_milestone_name,
            target_date=self.new_milestone_target_date,
            status=self.new_milestone_status,
            workstream_id=self.new_milestone_workstream,
        )
        self.milestones.append(new_milestone)
        self.milestone_modal_open = False

    def set_objective_modal_open(self, open: bool):
        self.objective_modal_open = open

    def set_new_objective_name(self, name: str):
        self.new_objective_name = name

    def set_new_objective_description(self, description: str):
        self.new_objective_description = description

    def set_new_objective_workstream(self, workstream_id: int):
        self.new_objective_workstream = workstream_id

    def set_new_objective_target_date(self, date: str):
        self.new_objective_target_date = date

    def set_new_objective_status(self, status: MilestoneStatusVar):
        self.new_objective_status = status

    def add_objective(self):
        new_objective = ObjectiveBase(
            objective_name=self.new_objective_name,
            description=self.new_objective_description,
            workstream_id=self.new_objective_workstream,
            target_date=self.new_objective_target_date,
            status=self.new_objective_status,
        )
        self.objectives.append(new_objective)
        self.objective_modal_open = False

    def set_selected_report_type(self, report_type: str):
        self.selected_report_type = report_type

    def generate_report(self):
        if self.selected_report_type == "Task Status Summary":
            self.generate_task_status_summary()
        elif self.selected_report_type == "Workstream Progress":
            self.generate_workstream_progress()
        elif self.selected_report_type == "Staff Workload":
            self.generate_staff_workload()
        elif self.selected_report_type == "Milestone Timeline":
            self.generate_milestone_timeline()
        elif self.selected_report_type == "Objective Status":
            self.generate_objective_status()

    @rx.var
    def generate_task_status_summary(self):
        status_counts = {}
        for task in self.tasks:
            status_counts[task.status] = status_counts.get(task.status, 0) + 1
        self.report_data = [
            {"Status": status, "Count": count}
            for status, count in status_counts.items()
        ]
        self.report_columns = [
            {"header": "Status", "accessor": "Status"},
            {"header": "Count", "accessor": "Count"},
        ]

    @rx.var
    def generate_workstream_progress(self):
        workstream_progress = {}
        for workstream in self.workstreams:
            total_tasks = len(
                [
                    task
                    for task in self.tasks
                    if task.workstream_id == workstream.workstream_id
                ]
            )
            completed_tasks = len(
                [
                    task
                    for task in self.tasks
                    if task.workstream_id == workstream.workstream_id
                    and task.status == "Completed"
                ]
            )
            progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            workstream_progress[workstream.workstream_name] = progress
        self.report_data = [
            {"Workstream": name, "Progress (%)": progress}
            for name, progress in workstream_progress.items()
        ]
        self.report_columns = [
            {"header": "Workstream", "accessor": "Workstream"},
            {"header": "Progress (%)", "accessor": "Progress (%)"},
        ]

    @rx.var
    def generate_staff_workload(self):
        staff_workload = {}
        for staff in self.staff_members:
            assigned_tasks = len(
                [
                    task
                    for task in self.tasks
                    if task.assigned_to == staff.staff_member_id
                ]
            )
            staff_workload[f"{staff.first_name} {staff.last_name}"] = assigned_tasks
        self.report_data = [
            {"Staff Member": name, "Assigned Tasks": count}
            for name, count in staff_workload.items()
        ]
        self.report_columns = [
            {"header": "Staff Member", "accessor": "Staff Member"},
            {"header": "Assigned Tasks", "accessor": "Assigned Tasks"},
        ]

    @rx.var
    def generate_milestone_timeline(self):
        self.report_data = [
            {
                "Milestone": milestone.milestone_name,
                "Target Date": milestone.target_date,
                "Status": milestone.status,
            }
            for milestone in sorted(self.milestones, key=lambda m: m.target_date)
        ]
        self.report_columns = [
            {"header": "Milestone", "accessor": "Milestone"},
            {"header": "Target Date", "accessor": "Target Date"},
            {"header": "Status", "accessor": "Status"},
        ]

    @rx.var
    def generate_objective_status(self):
        self.report_data = [
            {
                "Objective": objective.objective_name,
                "Status": objective.status,
                "Target Date": objective.target_date,
            }
            for objective in self.objectives
        ]
        self.report_columns = [
            {"header": "Objective", "accessor": "Objective"},
            {"header": "Status", "accessor": "Status"},
            {"header": "Target Date", "accessor": "Target Date"},
        ]

    @rx.var
    def get_workstream_progress(self):
        self.workstream_progress = []
        for workstream in self.workstreams:
            tasks = [t for t in self.tasks if t.workstream_id == workstream.workstream_id]
            total = len(tasks)
            completed = sum(1 for t in tasks if t.status == "Completed")
            progress = (completed / total * 100) if total > 0 else 0
            self.workstream_progress.append({
                "workstream": workstream.workstream_name,
                "progress": round(progress, 2),
                "total_tasks": total,
                "completed_tasks": completed
            })

    @rx.var
    def get_staff_workload(self):
        self.staff_workload = []
        for staff in self.staff_members:
            tasks = [t for t in self.tasks if t.assigned_to == staff.staff_member_id]
            self.staff_workload.append({
                "staff_name": f"{staff.first_name} {staff.last_name}",
                "total_tasks": len(tasks),
                "completed_tasks": sum(1 for t in tasks if t.status == "Completed"),
                "in_progress_tasks": sum(1 for t in tasks if t.status == "In Progress"),
                "not_started_tasks": sum(1 for t in tasks if t.status == "Not Started")
            })

    def get_all_tasks(self):
        response = supabase.table("tasks").select("*").execute()
        return [TaskBase(**task) for task in response.data]

    def get_all_workstreams(self):
        response = supabase.table("workstreams").select("*").execute()
        return [WorkstreamBase(**workstream) for workstream in response.data]

    def get_all_staff_members(self):
        response = supabase.table("staff_members").select("*").execute()
        return [StaffMemberBase(**staff_member) for staff_member in response.data]

    def get_all_milestones(self):
        response = supabase.table("milestones").select("*").execute()
        return [MilestoneBase(**milestone) for milestone in response.data]

    def get_all_objectives(self):
        response = supabase.table("objectives").select("*").execute()
        return [ObjectiveBase(**objective) for objective in response.data]

    def get_all_check_ins(self):
        response = supabase.table("check_ins").select("*").execute()
        return [CheckInBase(**check_in) for check_in in response.data]
