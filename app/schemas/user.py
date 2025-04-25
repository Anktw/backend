from typing import Optional
from pydantic import BaseModel, EmailStr

class StartRegistrationRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str
    timezone: str

class ResendOtpRequest(BaseModel):
    email: EmailStr

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    timezone: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class PasswordResetRequest(BaseModel):
    email_or_username: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    profile_picture_url: str | None = None
    location: str | None = None
    timezone: str | None = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


    class Config:
        from_attributes = True


    class Config:
        from_attributes = True