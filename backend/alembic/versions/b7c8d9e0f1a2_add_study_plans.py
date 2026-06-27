"""add study plans

Revision ID: b7c8d9e0f1a2
Revises: a1b2c3d4e5f7
Create Date: 2026-06-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7c8d9e0f1a2"
down_revision: Union[str, Sequence[str], None] = "a1b2c3d4e5f7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "study_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("subjects_json", sa.Text(), nullable=False),
        sa.Column("weekly_plan_json", sa.Text(), nullable=False),
        sa.Column("ai_reasoning", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_study_plans_id"), "study_plans", ["id"], unique=False)
    op.create_index(op.f("ix_study_plans_title"), "study_plans", ["title"], unique=False)
    op.create_index(op.f("ix_study_plans_user_id"), "study_plans", ["user_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_study_plans_user_id"), table_name="study_plans")
    op.drop_index(op.f("ix_study_plans_title"), table_name="study_plans")
    op.drop_index(op.f("ix_study_plans_id"), table_name="study_plans")
    op.drop_table("study_plans")
