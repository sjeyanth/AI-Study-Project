from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True, index=True)

    email = Column(String, unique=True, index=True)

    hashed_password = Column(String)

    tasks = relationship(
        "Task",
        back_populates="owner"
    )

    notes = relationship(
        "Note",
        back_populates="owner"
    )

    reminders = relationship(
        "Reminder",
        back_populates="owner"
    )

    budgets = relationship(
        "Budget",
        back_populates="owner"
    )

    expenses = relationship(
        "Expense",
        back_populates="owner"
    )

    goals = relationship(
        "Goal",
        back_populates="owner"
    )