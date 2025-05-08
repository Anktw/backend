from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import validates
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

    @validates('email')
    def lowercase_email(self, key, email):
        return email.lower()

    @validates('username')
    def lowercase_username(self, key, username):
        return username.lower()
    @validates('first_name', 'last_name')

    def validate_name(self, key, name):
        self.title = name.title()
        return name.title()
        