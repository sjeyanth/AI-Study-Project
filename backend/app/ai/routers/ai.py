from fastapi import APIRouter
from app.ai.services.ai_service import summarize_note

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
  request: NoteSummaryRequest
  ):
  
    summary=summarize_note(request.content)
    return {   #NotesummaryResponse(summary=summary)  #Notesummaryresponse is a pydantic model, we can return a dict and it will be converted to the model
        "summary": summary
    }
