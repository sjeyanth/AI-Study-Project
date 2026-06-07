from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int

    total_goals: int
    completed_goals: int

    average_goal_progress: float

    total_notes: int

    total_reminders: int
    upcoming_reminders: int

    total_budget: float
    total_spent: float
    remaining_budget: float
