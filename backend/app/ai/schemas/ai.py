from pydantic import BaseModel, Field


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
    tasks: list[str]


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


