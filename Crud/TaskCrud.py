from fastapi import HTTPException
from sqlalchemy.orm import Session
from Schemas.schemas import TaskCreate,TaskUpdate
from Models.models import Task
from datetime import datetime


def crud_create_task(task: TaskCreate,db: Session, current_user):
    task_db_info = Task(
        title=task.title,
        description=task.description,
        user_id=current_user.id,
        status = task.status ,
        created_at = task.due_date  
    )

    db.add(task_db_info)
    db.commit()
    db.refresh(task_db_info)

    return task_db_info

def crud_get_tasks(
    db: Session, current_user , status,page,limit,sort
):
    offset = (page -1) * limit
    query = db.query(Task).filter(Task.user_id == current_user.id)
    if status:
        query = query.filter(Task.status == status)
    if sort == "asc":
        query = query.order_by(Task.created_at.asc())
    else:
        query = query.order_by(Task.created_at.desc())

    return query.offset(offset).limit(limit).all()

def crud_update_task(
    task_id: str, task: TaskUpdate, db: Session, current_user
):
    existing_task = db.query(Task).filter(Task.id == task_id).first()

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if existing_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.status = task.status

    db.commit()
    db.refresh(existing_task)

    return existing_task


def crud_delete_task(
     task_id: str,db: Session, current_user
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}

def get_overdue(db: Session, current_user):
    return db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status != "completed",
        Task.due_date < datetime.utcnow()
    ).all()