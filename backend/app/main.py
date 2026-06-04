from fastapi import FastAPI
from app.routers.notes import router as notes_router
from app.routers.reminders import router as reminders_router
from app.routers.tasks import router as tasks_router
from app.routers.users import router as users_router


app = FastAPI()

app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(notes_router)
app.include_router(reminders_router)


@app.get("/")
def root():
    return {"message": "Backend running successfully!"}