from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int

    total_goals: int
    completed_goals: int

    average_goal_progress: float