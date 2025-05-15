from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"
    taskid = Column(Integer, primary_key=True, index=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    name = Column(String, nullable=False)
    estimated_time = Column(Integer, nullable=False)
    completion_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed = Column(Boolean, default=False)
    taskidbyfrontend = Column(Integer, nullable=True)

class SavedTask(Base):
    __tablename__ = "saved_tasks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)
    name = Column(String, nullable=False)
    estimated_time = Column(Integer, nullable=False)
