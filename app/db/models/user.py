from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, func
from app.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    

    # Core Login/Identity
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)

    # Personal Details
    first_name = Column(String, nullable=True, default=None)
    last_name = Column(String, nullable=True, default=None)
    profile_picture_url = Column(String, nullable=True)
    location = Column(String, nullable=True, default=None)

    # Account Status & Metadata
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    timezone = Column(String(50), nullable=True, default='UTC')

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True, default=None)
    last_login_at = Column(DateTime(timezone=True), nullable=True, default=None)


class PendingUser(Base):
    __tablename__ = "pending_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    otp = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)