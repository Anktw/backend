from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, Token, PasswordResetRequest, PasswordResetConfirm
from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token, get_password_hash, create_password_reset_token, verify_password_reset_token
from app.services.email import send_reset_email

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, user_in)
    token = create_access_token({"sub": user.email})
    return {"access_token": token}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token}

@router.post("/request-password-reset")
def request_password_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = create_password_reset_token(user.email)
    send_reset_email(user.email, reset_token)
    return {"msg": "Password reset email sent"}

@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    email = verify_password_reset_token(data.token)
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    return {"msg": "Password updated successfully"}