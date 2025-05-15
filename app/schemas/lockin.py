from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    estimated_time: int
    completion_time: Optional[datetime] = None
    completed: Optional[bool] = False
    taskidbyfrontend: int

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    estimated_time: Optional[int] = None
    completion_time: Optional[datetime] = None
    completed: Optional[bool] = None
    taskidbyfrontend: Optional[int] = None

class TaskOut(BaseModel):
    taskid: int
    username: str
    estimated_time: int
    completion_time: Optional[datetime]
    completed: bool
    created_at: datetime
    taskidbyfrontend: int
    
    class Config:
        from_attributes = True

# --- SavedTask Schemas ---
class SavedTaskBase(BaseModel):
    username: str
    name: str
    estimated_time: int
    taskidbyfrontend: int

class SavedTaskCreate(SavedTaskBase):
    pass

class SavedTaskUpdate(BaseModel):
    name: Optional[str] = None
    estimated_time: Optional[int] = None
    taskidbyfrontend: Optional[int] = None

class SavedTaskOut(SavedTaskBase):
    class Config:
        from_attributes = True
