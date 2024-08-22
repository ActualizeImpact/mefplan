from typing import Literal, Optional
import reflex as rx

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


class ReportBase(rx.Base):
    report_id: Optional[int] = None
    report_title: str
    report_date: str
    report_content: Optional[str] = None
    created_by: int


class MeetingBase(rx.Base):
    meeting_id: Optional[int] = None
    meeting_title: str
    meeting_date: str
    meeting_notes: Optional[str] = None
    participants: Optional[str] = None
    workstream_id: int


class MilestoneBase(rx.Base):
    milestone_id: Optional[int] = None
    milestone_name: str
    target_date: str
    status: MilestoneStatusVar
    workstream_id: int
    objective_id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class KPIBase(rx.Base):
    kpi_id: Optional[int] = None
    kpi_name: str
    target: str
    current_value: Optional[str] = None
    workstream_id: int


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
