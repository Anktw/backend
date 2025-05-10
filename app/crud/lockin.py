from sqlalchemy.orm import Session
from app.db.models.lockin import Task, SavedTask
from typing import List, Optional

# Helper to get model columns (excluding PKs)
def _get_updatable_fields(model, exclude: set = None):
    exclude = exclude or set()
    return {
        c.name for c in model.__table__.columns
        if not c.primary_key and c.name not in exclude
    }

def get_tasks_by_user(db: Session, username: str) -> List[Task]:
    return db.query(Task).filter(Task.username == username).all()

def update_task_by_id(db: Session, username: str, taskid: int, data: dict) -> Optional[Task]:
    task = db.query(Task).filter(Task.taskid == taskid, Task.username == username).first()
    if not task:
        return None
    allowed_fields = _get_updatable_fields(Task, exclude={"username", "created_at"})
    for field, value in data.items():
        if field in allowed_fields:
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
    allowed_fields = _get_updatable_fields(SavedTask, exclude={"username"})
    for field, value in data.items():
        if field in allowed_fields:
            setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task
