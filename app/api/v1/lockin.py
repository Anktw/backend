from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.lockin import Task, SavedTask
from app.db.session import SessionLocal
from app.schemas.lockin import TaskOut, TaskCreate, TaskUpdate, SavedTaskOut, SavedTaskCreate, SavedTaskUpdate
from app.api.deps import get_db, get_current_user
from typing import List

router = APIRouter()

@router.post("/tasks", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = Task(
        username=current_user.username,
        name=payload.name,
        estimated_time=payload.estimated_time,
        completion_time=payload.completion_time,
        completed=payload.completed,
        taskidbyfrontend=payload.taskidbyfrontend,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/tasks", response_model=List[TaskOut])
def get_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.username == current_user.username).all()
    return tasks

@router.put("/tasks/{taskidbyfrontend}", response_model=TaskOut)
def update_task(taskidbyfrontend: int, payload: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.taskidbyfrontend == taskidbyfrontend, Task.username == current_user.username).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{taskidbyfrontend}", response_model=TaskOut)
def delete_task(taskidbyfrontend: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.taskidbyfrontend == taskidbyfrontend, Task.username == current_user.username).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return task

@router.post("/saved-tasks", response_model=SavedTaskOut)
def create_saved_task(payload: SavedTaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = SavedTask(
        username=current_user.username,
        name=payload.name,
        estimated_time=payload.estimated_time,
        taskidbyfrontend=payload.taskidbyfrontend,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/saved-tasks", response_model=List[SavedTaskOut])
def get_saved_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = db.query(SavedTask).filter(SavedTask.username == current_user.username).all()
    return tasks

@router.put("/saved-tasks/{taskidbyfrontend}", response_model=SavedTaskOut)
def update_saved_task(taskidbyfrontend: int, payload: SavedTaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(SavedTask).filter(SavedTask.taskidbyfrontend == taskidbyfrontend, SavedTask.username == current_user.username).first()
    if not task:
        raise HTTPException(status_code=404, detail="SavedTask not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/saved-tasks/{taskidbyfrontend}", response_model=SavedTaskOut)
def delete_saved_task_by_frontend_id(taskidbyfrontend: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(SavedTask).filter(SavedTask.taskidbyfrontend == taskidbyfrontend, SavedTask.username == current_user.username).first()
    if not task:
        raise HTTPException(status_code=404, detail="SavedTask not found")
    db.delete(task)
    db.commit()
    return task