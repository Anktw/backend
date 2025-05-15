from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.lockin import Task, SavedTask
from app.db.session import SessionLocal
from app.schemas.lockin import TaskOut, TaskCreate, TaskUpdate, SavedTaskOut, SavedTaskCreate, SavedTaskUpdate
from app.api.deps import get_db, get_current_user
from typing import List
from pydantic import BaseModel

class DeleteResponse(BaseModel):
    message: str
    taskidbyfrontend: int

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
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

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

@router.delete("/tasks/{taskidbyfrontend}", response_model=DeleteResponse)
def delete_task(taskidbyfrontend: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.taskidbyfrontend == taskidbyfrontend, Task.username == current_user.username).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return DeleteResponse(message="Task deleted successfully", taskidbyfrontend=taskidbyfrontend)

@router.post("/saved-tasks", response_model=SavedTaskOut)
def create_saved_task(payload: SavedTaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = SavedTask(
        username=current_user.username,
        name=payload.name,
        estimated_time=payload.estimated_time,
    )
    db.add(task)
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

@router.delete("/saved-tasks/{id}", response_model=BaseModel)
def delete_saved_task_by_id(id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(SavedTask).filter(SavedTask.id == id, SavedTask.username == current_user.username).first()
    if not task:
        raise HTTPException(status_code=404, detail="SavedTask not found")
    db.delete(task)
    db.commit()
    return {"message": "Saved task deleted successfully", "id": id}