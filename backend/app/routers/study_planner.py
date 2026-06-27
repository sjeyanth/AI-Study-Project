from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.auth_dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.study_plan import (
    CreateStudyPlan,
    StudyPlanResponse,
    StudyPlanSummary
)
from app.services import study_plan_service


router = APIRouter()


@router.post(
    "/study-planner",
    response_model=StudyPlanResponse,
    status_code=status.HTTP_201_CREATED
)
def create_study_plan(
    request: CreateStudyPlan,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return study_plan_service.create_study_plan(
        db,
        request,
        current_user
    )


@router.get(
    "/study-planner",
    response_model=list[StudyPlanSummary]
)
def get_study_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return study_plan_service.get_all_study_plans(
        db,
        current_user
    )


@router.get(
    "/study-planner/{study_plan_id}",
    response_model=StudyPlanResponse
)
def get_study_plan(
    study_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return study_plan_service.get_study_plan_by_id(
        study_plan_id,
        db,
        current_user
    )


@router.delete(
    "/study-planner/{study_plan_id}"
)
def delete_study_plan(
    study_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return study_plan_service.delete_study_plan(
        study_plan_id,
        db,
        current_user
    )
