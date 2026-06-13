from pydantic import BaseModel, Field


class AssistantChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1
    )


class AssistantChatResponse(BaseModel):
    response: str