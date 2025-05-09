from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    username: str
    estimated_time: int
    completion_time: Optional[datetime] = None
    completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    estimated_time: Optional[int] = None
    completion_time: Optional[datetime] = None
    completed: Optional[bool] = None

class TaskOut(TaskBase):
    taskid: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- SavedTask Schemas ---
class SavedTaskBase(BaseModel):
    username: str
    name: str
    estimated_time: int

class SavedTaskCreate(SavedTaskBase):
    pass

class SavedTaskUpdate(BaseModel):
    name: Optional[str] = None
    estimated_time: Optional[int] = None

class SavedTaskOut(SavedTaskBase):
    id: int

    class Config:
        from_attributes = True
