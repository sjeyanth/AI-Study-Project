"""add budgets and expenses

Revision ID: d6f7a8b9c0d1
Revises: f1b2c3d4e5f6
Create Date: 2026-06-05 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d6f7a8b9c0d1"
down_revision: Union[str, Sequence[str], None] = "f1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "budgets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("month", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("total_budget", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="INR"),
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
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_budgets_id"), "budgets", ["id"], unique=False)
    op.create_index(op.f("ix_budgets_month"), "budgets", ["month"], unique=False)
    op.create_index(op.f("ix_budgets_year"), "budgets", ["year"], unique=False)
    op.create_index(op.f("ix_budgets_user_id"), "budgets", ["user_id"], unique=False)

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("expense_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("notes", sa.String(length=1000), nullable=True),
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
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_expenses_id"), "expenses", ["id"], unique=False)
    op.create_index(op.f("ix_expenses_title"), "expenses", ["title"], unique=False)
    op.create_index(op.f("ix_expenses_category"), "expenses", ["category"], unique=False)
    op.create_index(op.f("ix_expenses_expense_date"), "expenses", ["expense_date"], unique=False)
    op.create_index(op.f("ix_expenses_user_id"), "expenses", ["user_id"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_expenses_user_id"), table_name="expenses")
    op.drop_index(op.f("ix_expenses_expense_date"), table_name="expenses")
    op.drop_index(op.f("ix_expenses_category"), table_name="expenses")
    op.drop_index(op.f("ix_expenses_title"), table_name="expenses")
    op.drop_index(op.f("ix_expenses_id"), table_name="expenses")
    op.drop_table("expenses")

    op.drop_index(op.f("ix_budgets_user_id"), table_name="budgets")
    op.drop_index(op.f("ix_budgets_year"), table_name="budgets")
    op.drop_index(op.f("ix_budgets_month"), table_name="budgets")
    op.drop_index(op.f("ix_budgets_id"), table_name="budgets")
    op.drop_table("budgets")
