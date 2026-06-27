from urllib import request

from fastapi import APIRouter, Depends
from app.ai.services.ai_service import summarize_note, generate_mail, task_breakdown, budget_insights


from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.auth_dependencies import get_current_user

from app.models.user import User


from app.ai.schemas.ai import (
    NoteSummaryRequest,
    NoteSummaryResponse,
    EmailGenerationRequest,
    EmailGenerationResponse,
    TaskBreakdownRequest,
    TaskBreakdownResponse,
    BudgetInsightsRequest,
    BudgetInsightsResponse
)

router =APIRouter(prefix="/ai", tags=["AI"])

@router.post("/summarize-note", response_model=NoteSummaryResponse)
def summarize_note_route(
  request: NoteSummaryRequest,
  current_user: User = Depends(get_current_user)
  ):
  
    summary=summarize_note(request.content)
    return {   #NotesummaryResponse(summary=summary)  #Notesummaryresponse is a pydantic model, we can return a dict and it will be converted to the model
        "summary": summary
    }


@router.post("/generate-mail", response_model=EmailGenerationResponse)

def generate_mail_route(
    request: EmailGenerationRequest,
    current_user: User = Depends(get_current_user)
):

    email = generate_mail(
        request.purpose
    )
    #current_user: User = Depends(get_current_user)

    return {
        "email": email
    }

@router.post(
    "/task-breakdown",
    response_model=TaskBreakdownResponse
)
def task_breakdown_route(
    request: TaskBreakdownRequest,
    current_user: User = Depends(get_current_user)
):

    tasks = task_breakdown(
        request.goal
    )
    return {
        "tasks": tasks
    }

@router.post(
    "/budget-insights",
    response_model=BudgetInsightsResponse
)
def budget_insights_route(
    request: BudgetInsightsRequest,
    current_user: User = Depends(get_current_user)
):

    insights = budget_insights(
        request.budget_summary
    )
    return {
        "insights": insights
    }
