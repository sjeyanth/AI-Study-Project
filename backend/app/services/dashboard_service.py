from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.task import Task
from app.models.goal import Goal
from app.models.user import User
from app.models.budget import Budget
from app.models.expense import Expense
from app.models.reminder import Reminder
from app.models.note import Note


def get_dashboard_data(
    db: Session,
    current_user: User
):

    total_tasks = db.query(
        func.count(Task.id)
    ).filter(
        Task.user_id == current_user.id
    ).scalar()

    completed_tasks = db.query(
        func.count(Task.id)
    ).filter(
        Task.user_id == current_user.id,
        Task.completed == True
    ).scalar()

    pending_tasks = db.query(
        func.count(Task.id)
    ).filter(
        Task.user_id == current_user.id,
        Task.completed == False
    ).scalar()

    total_goals = db.query(
        func.count(Goal.id)
    ).filter(
        Goal.user_id == current_user.id
    ).scalar()

    completed_goals = db.query(
        func.count(Goal.id)
    ).filter(
        Goal.user_id == current_user.id,
        Goal.status == "completed"
    ).scalar()

    average_goal_progress = db.query(
        func.avg(Goal.progress)
    ).filter(
        Goal.user_id == current_user.id
    ).scalar()

    average_goal_progress = (
        average_goal_progress or 0
    )

    total_notes = db.query(
        func.count(Note.id)
    ).filter(
        Note.user_id == current_user.id
    ).scalar()

    total_reminders = db.query(
        func.count(Reminder.id)
    ).filter(
        Reminder.user_id == current_user.id
    )   .scalar()


    upcoming_reminders = db.query(
        func.count(Reminder.id)
    ).filter(
        Reminder.user_id == current_user.id,
        Reminder.due_date > func.now()
    ).scalar()


    budget = db.query(Budget).filter(
        Budget.user_id == current_user.id
    ).first()
    total_budget = (
    budget.total_budget
    if budget
    else 0
  )
    

    total_spent = db.query(
    func.sum(Expense.amount)
    ).filter(
      Expense.user_id == current_user.id
    ).scalar()
    total_spent = total_spent or 0

    remaining_budget = total_budget - total_spent
  
    


    return {
    "total_tasks": total_tasks,
    "completed_tasks": completed_tasks,
    "pending_tasks": pending_tasks,

    "total_goals": total_goals,
    "completed_goals": completed_goals,
    "average_goal_progress": round(
        average_goal_progress,
        2
    ),

    "total_notes": total_notes,

    "total_reminders": total_reminders,
    "upcoming_reminders": upcoming_reminders,

    "total_budget": total_budget,
    "total_spent": total_spent,
    "remaining_budget": remaining_budget
    }