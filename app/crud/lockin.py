from sqlalchemy.orm import Session
from app.db.models.lockin import Task, SavedTask
from typing import List, Optional

def get_tasks_by_user(db: Session, username: str) -> List[Task]:
    return db.query(Task).filter(Task.username == username).all()

def update_task_by_id(db: Session, username: str, taskid: int, data: dict) -> Optional[Task]:
    task = db.query(Task).filter(Task.taskid == taskid, Task.username == username).first()
    if not task:
        return None
    for field, value in data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def get_saved_tasks_by_user(db: Session, username: str) -> List[SavedTask]:
    return db.query(SavedTask).filter(SavedTask.username == username).all()

def update_saved_task_by_id(db: Session, username: str, id: int, data: dict) -> Optional[SavedTask]:
    task = db.query(SavedTask).filter(SavedTask.id == id, SavedTask.username == username).first()
    if not task:
        return None
    for field, value in data.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task
