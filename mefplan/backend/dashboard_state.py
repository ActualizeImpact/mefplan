import reflex as rx
import datetime
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class DashboardState(rx.State):
    total_tasks: int = 0
    tasks_by_status: list = []
    workstream_progress: list = []
    upcoming_milestones: list = []
    staff_workload: list = []
    recent_activity: list = []
    selected_tab: str = "tasks"
    area_toggle: bool = True

    def fetch_data(self):
        self.fetch_total_tasks()
        self.fetch_tasks_by_status()
        self.fetch_workstream_progress()
        self.fetch_upcoming_milestones()
        self.fetch_staff_workload()
        self.fetch_recent_activity()

    def fetch_total_tasks(self):
        response = supabase.table("tasks").select("count", count="exact").execute()
        self.total_tasks = response.count

    def fetch_tasks_by_status(self):
        response = (
            supabase.table("tasks").select("status, count").group_by("status").execute()
        )
        self.tasks_by_status = [
            {"name": item["status"], "value": item["count"]} for item in response.data
        ]

    def fetch_workstream_progress(self):
        response = supabase.table("workstreams").select("workstream_id, name").execute()
        workstreams = response.data

        self.workstream_progress = []
        for ws in workstreams:
            total_tasks = (
                supabase.table("tasks")
                .select("count", count="exact")
                .eq("workstream_id", ws["workstream_id"])
                .execute()
                .count
            )
            completed_tasks = (
                supabase.table("tasks")
                .select("count", count="exact")
                .eq("workstream_id", ws["workstream_id"])
                .eq("status", "Completed")
                .execute()
                .count
            )
            progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            self.workstream_progress.append(
                {"workstream": ws["name"], "progress": round(progress, 2)}
            )

    def fetch_upcoming_milestones(self):
        today = datetime.date.today()
        thirty_days_later = today + datetime.timedelta(days=30)
        response = (
            supabase.table("milestones")
            .select("name, target_date")
            .gte("target_date", today)
            .lte("target_date", thirty_days_later)
            .order("target_date")
            .limit(5)
            .execute()
        )
        self.upcoming_milestones = [
            {"Milestone": item["name"], "Target Date": item["target_date"]}
            for item in response.data
        ]

    def fetch_staff_workload(self):
        response = (
            supabase.table("staff_members")
            .select("staff_member_id, first_name, last_name")
            .execute()
        )
        staff_members = response.data

        self.staff_workload = []
        for staff in staff_members:
            tasks_count = (
                supabase.table("tasks")
                .select("count", count="exact")
                .eq("assigned_to", staff["staff_member_id"])
                .execute()
                .count
            )
            self.staff_workload.append(
                {
                    "staff": f"{staff['first_name']} {staff['last_name']}",
                    "tasks": tasks_count,
                }
            )

    def fetch_recent_activity(self):
        # This is a simplified version. You might want to create a separate "activities" table for more detailed tracking
        response = (
            supabase.table("tasks")
            .select("task_name, status, updated_at")
            .order("updated_at", desc=True)
            .limit(5)
            .execute()
        )
        self.recent_activity = [
            f"Task '{item['task_name']}' {item['status']}" for item in response.data
        ]

    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle
