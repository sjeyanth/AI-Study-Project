from copy import error

from  app.ai.services.note_ai_service import  summarize_notes_with_ai
from  app.ai.services.email_ai_service import  generate_email_with_ai
from  app.ai.services.task_breakdown_ai_service import task_breakdown_with_ai
from app.ai.schemas.ai import StudyPlannerRequest, StudyPlannerResponse
from app.ai.services.study_planner_ai_service import (
    build_fallback_study_plan,
    generate_study_plan_with_ai
)


def summarize_note(
    content: str
):

    try:

        return summarize_notes_with_ai(
            content
        )

    except Exception as error:

        print(
            f"Note AI Error: {error}"
        )

        return (
            f"Mock Summary: "
            f"{content[:100]}"
        )

def generate_mail(
    purpose: str
):

    try:

        return generate_email_with_ai(
            purpose
        )

    except Exception as error:

        print(
            f"Email AI Error: {error}"
        )

        return (
            f"Mock Email for: "
            f"{purpose}"
        )

def task_breakdown(
        goal: str
) -> str:
    
    try:

        return task_breakdown_with_ai(
        goal
    )

    except Exception as error:

        print(
        f"Task AI Error: {error}"
    )

    return (
        f"Mock Task Breakdown "
        f"for: {goal}"
    )


def budget_insights(
    budget_summary: str
) -> str:

    return (
        "Mock Insight: "
        "Monitor your spending and "
        "reduce unnecessary expenses."
    )


def study_planner(
    request: StudyPlannerRequest
) -> StudyPlannerResponse:

    try:

        plan = generate_study_plan_with_ai(
            request
        )
        return StudyPlannerResponse(
            **plan
        )

    except Exception as error:

        print(
            f"Study Planner AI Error: {error}"
        )
        plan = build_fallback_study_plan(
            request
        )

    return StudyPlannerResponse(
        **plan
    )


