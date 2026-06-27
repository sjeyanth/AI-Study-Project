from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.ai.schemas.ai import (
    AssignmentDeadlineRequest,
    StudyPlannerResponse,
    StudySubjectRequest,
    SessionLength
)


class CreateStudyPlan(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    subjects: List[StudySubjectRequest] = Field(..., min_items=1, max_items=12)
    assignment_deadlines: List[AssignmentDeadlineRequest] = Field(
        default_factory=list,
        max_items=20
    )
    available_hours_per_day: float = Field(..., ge=0.5, le=16)
    preferred_session_length: SessionLength
    notes: Optional[str] = Field(default=None, max_length=1000)


class StudyPlanSummary(BaseModel):
    id: int
    title: str
    subject_count: int
    created_at: datetime
    updated_at: datetime


class StudyPlanResponse(StudyPlanSummary):
    subjects_json: List[StudySubjectRequest]
    weekly_plan_json: StudyPlannerResponse
    ai_reasoning: str

