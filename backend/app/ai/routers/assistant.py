from fastapi import (
    APIRouter,
    Depends
)

from app.database.auth_dependencies import (
    get_current_user
)

from app.models.user import User

from app.ai.schemas.assistant import (
    AssistantChatRequest,
    AssistantChatResponse
)

from app.ai.services.assistant_service import (
    chat
)

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"]
)


@router.post(
    "/chat",
    response_model=AssistantChatResponse
)
def assistant_chat(
    request: AssistantChatRequest,
    current_user: User = Depends(
        get_current_user
    )
):

    response = chat(
        request.message
    )

    return {
        "response": response
    }