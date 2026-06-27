from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


from app.routers.budgets import router as budgets_router
from app.routers.expenses import router as expenses_router
from app.routers.goals import router as goals_router
from app.routers.notes import router as notes_router
from app.routers.reminders import router as reminders_router
from app.routers.study_planner import router as study_planner_router
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router
from app.schemas.dashboard import DashboardResponse
from app.routers.dashboard import router as dashboard_router
from app.ai.routers.ai import router as ai_router
from app.ai.routers.assistant import (router as assistant_router)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(notes_router)
app.include_router(reminders_router)
app.include_router(budgets_router)
app.include_router(expenses_router)
app.include_router(goals_router)
app.include_router(dashboard_router)
app.include_router(study_planner_router)
app.include_router(ai_router)
app.include_router(assistant_router)
@app.get("/")
def root():
    return {"message": "Backend running successfully!"}
