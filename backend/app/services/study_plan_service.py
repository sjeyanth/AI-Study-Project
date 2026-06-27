import json

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.ai.schemas.ai import StudyPlannerRequest, StudyPlannerResponse
from app.ai.services.ai_service import study_planner
from app.models.study_plan import StudyPlan as StudyPlanModel
from app.models.user import User
from app.schemas.study_plan import (
    CreateStudyPlan,
    StudyPlanResponse,
    StudyPlanSummary
)


def create_study_plan(
    db: Session,
    request: CreateStudyPlan,
    current_user: User
) -> StudyPlanResponse:

    ai_request = StudyPlannerRequest(
        subjects=request.subjects,
        assignment_deadlines=request.assignment_deadlines,
        available_hours_per_day=request.available_hours_per_day,
        preferred_session_length=request.preferred_session_length,
        notes=request.notes
    )
    generated_plan = study_planner(
        ai_request
    )
    title = request.title.strip() if request.title else _build_title(
        request
    )

    study_plan = StudyPlanModel(
        user_id=current_user.id,
        title=title,
        subjects_json=json.dumps(
            [
                subject.dict()
                for subject in request.subjects
            ],
            default=str
        ),
        weekly_plan_json=generated_plan.json(),
        ai_reasoning=generated_plan.explanation
    )

    try:
        db.add(
            study_plan
        )
        db.commit()
        db.refresh(
            study_plan
        )
    except SQLAlchemyError as error:
        db.rollback()
        print(
            f"Study plan database error: {error}"
        )
        raise HTTPException(
            status_code=500,
            detail="Unable to save study plan"
        )

    return _to_response(
        study_plan
    )


def get_all_study_plans(
    db: Session,
    current_user: User
) -> list[StudyPlanSummary]:

    plans = db.query(StudyPlanModel).filter(
        StudyPlanModel.user_id == current_user.id
    ).order_by(
        StudyPlanModel.created_at.desc()
    ).all()

    return [
        _to_summary(
            plan
        )
        for plan in plans
    ]


def get_study_plan_by_id(
    study_plan_id: int,
    db: Session,
    current_user: User
) -> StudyPlanResponse:

    study_plan = _get_owned_study_plan(
        study_plan_id,
        db,
        current_user
    )

    return _to_response(
        study_plan
    )


def delete_study_plan(
    study_plan_id: int,
    db: Session,
    current_user: User
):

    study_plan = _get_owned_study_plan(
        study_plan_id,
        db,
        current_user
    )

    try:
        db.delete(
            study_plan
        )
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        print(
            f"Study plan delete database error: {error}"
        )
        raise HTTPException(
            status_code=500,
            detail="Unable to delete study plan"
        )

    return {
        "message": "Study plan deleted successfully"
    }


def _get_owned_study_plan(
    study_plan_id: int,
    db: Session,
    current_user: User
) -> StudyPlanModel:

    study_plan = db.query(StudyPlanModel).filter(
        StudyPlanModel.id == study_plan_id,
        StudyPlanModel.user_id == current_user.id
    ).first()

    if study_plan is None:
        raise HTTPException(
            status_code=404,
            detail="Study plan not found"
        )

    return study_plan


def _to_summary(
    study_plan: StudyPlanModel
) -> StudyPlanSummary:

    subjects = _load_subjects(
        study_plan
    )

    return StudyPlanSummary(
        id=study_plan.id,
        title=study_plan.title,
        subject_count=len(
            subjects
        ),
        created_at=study_plan.created_at,
        updated_at=study_plan.updated_at
    )


def _to_response(
    study_plan: StudyPlanModel
) -> StudyPlanResponse:

    subjects = _load_subjects(
        study_plan
    )
    weekly_plan = StudyPlannerResponse(
        **json.loads(
            study_plan.weekly_plan_json
        )
    )

    return StudyPlanResponse(
        id=study_plan.id,
        title=study_plan.title,
        subject_count=len(
            subjects
        ),
        subjects_json=subjects,
        weekly_plan_json=weekly_plan,
        ai_reasoning=study_plan.ai_reasoning,
        created_at=study_plan.created_at,
        updated_at=study_plan.updated_at
    )


def _load_subjects(
    study_plan: StudyPlanModel
):

    return json.loads(
        study_plan.subjects_json
    )


def _build_title(
    request: CreateStudyPlan
) -> str:

    subject_names = [
        subject.name
        for subject in request.subjects[:3]
    ]

    title = "Study Plan: " + ", ".join(
        subject_names
    )

    if len(
        title
    ) > 200:
        return title[:197] + "..."

    return title
