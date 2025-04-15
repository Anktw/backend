from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    

    # Core Login/Identity
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True) # Optional unique username

    # Personal Details
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    phone_number = Column(String, index=True, nullable=True) # Consider uniqueness/validation
    bio = Column(Text, nullable=True)
    location = Column(String, nullable=True)

    # Account Status & Metadata
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    email_verified = Column(Boolean, default=False, nullable=True)
    language = Column(String(10), nullable=True)
    timezone = Column(String(50), nullable=True, default='UTC')

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    #social Links
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    portfolio_url = Column(String, nullable=True)
