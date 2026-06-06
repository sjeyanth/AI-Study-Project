from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.auth_dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate
from app.services import goal_service


router = APIRouter()


@router.get("/goals", response_model=list[GoalResponse])
def get_goals(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str | None = None,
    sort_by: str = Query("created_at"),
    sort_dir: str = Query("desc"),
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return goal_service.get_all_goals(
        db,
        current_user,
        skip,
        limit,
        status,
        sort_by,
        sort_dir,
        search
    )


@router.get("/goals/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return goal_service.get_goal_by_id(
        goal_id,
        db,
        current_user
    )


@router.post("/goals", response_model=GoalResponse)
def create_goal(
    goal: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return goal_service.create_goal(
        db,
        goal,
        current_user
    )


@router.put("/goals/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: int,
    updated_goal: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return goal_service.update_goal(
        goal_id,
        updated_goal,
        db,
        current_user
    )


@router.delete("/goals/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return goal_service.delete_goal(
        goal_id,
        db,
        current_user
    )