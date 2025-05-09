from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.lockin import Task, SavedTask
from app.db.session import SessionLocal
from app.schemas.lockin import TaskOut, TaskCreate, TaskUpdate, SavedTaskOut, SavedTaskCreate, SavedTaskUpdate
from app.api.deps import get_db, get_current_user
from typing import List

router = APIRouter()

@router.get("/tasks", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.username == current_user.username).all()
    return tasks

@router.put("/tasks/{taskid}", response_model=TaskOut)
def update_task(taskid: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.taskid == taskid, Task.username == current_user.username).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@router.get("/saved-tasks", response_model=List[SavedTaskOut])
def get_saved_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = db.query(SavedTask).filter(SavedTask.username == current_user.username).all()
    return tasks

@router.put("/saved-tasks/{id}", response_model=SavedTaskOut)
def update_saved_task(id: int, payload: SavedTaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(SavedTask).filter(SavedTask.id == id, SavedTask.username == current_user.username).first()
    if not task:
        raise HTTPException(status_code=404, detail="SavedTask not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task