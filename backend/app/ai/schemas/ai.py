from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, validator


# ==========================
# Note Summarizer
# ==========================

class NoteSummaryRequest(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        description="Note content to summarize"
    )


class NoteSummaryResponse(BaseModel):
    summary: str


# ==========================
# Email Generator
# ==========================

class EmailGenerationRequest(BaseModel):
    purpose: str = Field(
        ...,
        min_length=1,
        description="Purpose of the email"
    )


class EmailGenerationResponse(BaseModel):
    email: str


# ==========================
# Task Breakdown
# ==========================

class TaskBreakdownRequest(BaseModel):
    goal: str = Field(
        ...,
        min_length=1,
        description="Goal to break into tasks"
    )


class TaskBreakdownResponse(BaseModel):
    tasks: str


# ==========================
# Budget Insights
# ==========================

class BudgetInsightsRequest(BaseModel):
    budget_summary: str = Field(
        ...,
        min_length=1,
        description="Budget and spending summary"
    )


class BudgetInsightsResponse(BaseModel):
    insights: str


# ==========================
# Study Planner
# ==========================

DifficultyLevel = Literal["Easy", "Medium", "Hard"]
SessionLength = Literal[30, 45, 60, 90]


class StudySubjectRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=120,
        description="Subject name"
    )
    exam_date: date = Field(
        ...,
        description="Subject exam date"
    )
    difficulty: DifficultyLevel = Field(
        ...,
        description="Subject difficulty"
    )

    @validator("name")
    def subject_name_must_not_be_blank(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Subject name cannot be blank.")

        return cleaned_value

    @validator("exam_date")
    def exam_date_cannot_be_in_the_past(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Exam date cannot be in the past.")

        return value


class AssignmentDeadlineRequest(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=160,
        description="Assignment title"
    )
    subject: Optional[str] = Field(
        default=None,
        max_length=120,
        description="Related subject"
    )
    due_date: date = Field(
        ...,
        description="Assignment deadline"
    )

    @validator("title")
    def assignment_title_must_not_be_blank(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Assignment title cannot be blank.")

        return cleaned_value

    @validator("subject")
    def assignment_subject_must_not_be_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        cleaned_value = value.strip()

        return cleaned_value or None

    @validator("due_date")
    def deadline_cannot_be_in_the_past(cls, value: date) -> date:
        if value < date.today():
            raise ValueError("Assignment deadline cannot be in the past.")

        return value


class StudyPlannerRequest(BaseModel):
    subjects: List[StudySubjectRequest] = Field(
        ...,
        min_items=1,
        max_items=12,
        description="Subjects to plan for"
    )
    assignment_deadlines: List[AssignmentDeadlineRequest] = Field(
        default_factory=list,
        max_items=20,
        description="Optional assignment deadlines"
    )
    available_hours_per_day: float = Field(
        ...,
        ge=0.5,
        le=16,
        description="Available study hours per day"
    )
    preferred_session_length: SessionLength = Field(
        ...,
        description="Preferred study session length in minutes"
    )
    notes: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional planning notes"
    )

    @validator("notes")
    def notes_must_not_be_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        cleaned_value = value.strip()

        return cleaned_value or None


class StudyScheduleItem(BaseModel):
    subject: str
    duration_minutes: int = Field(..., ge=1)
    activity: str
    type: Literal["study", "revision", "assignment", "break"]


class WeeklyStudyDay(BaseModel):
    day: str
    total_minutes: int = Field(..., ge=0)
    sessions: List[StudyScheduleItem]


class DailyStudyPlan(BaseModel):
    date: str
    focus: str
    sessions: List[StudyScheduleItem]


class SubjectPriority(BaseModel):
    subject: str
    reason: str
    rank: int = Field(..., ge=1)


class RecommendedStudyDuration(BaseModel):
    subject: str
    minutes_per_week: int = Field(..., ge=0)
    reason: str


class RevisionItem(BaseModel):
    subject: str
    date: str
    focus: str


class StudyPlannerResponse(BaseModel):
    weekly_schedule: List[WeeklyStudyDay]
    daily_plan: List[DailyStudyPlan]
    priority_order: List[SubjectPriority]
    recommended_study_duration: List[RecommendedStudyDuration]
    revision_schedule: List[RevisionItem]
    break_suggestions: List[str]
    study_tips: List[str]
    explanation: str


