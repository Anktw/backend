from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.user import User
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, Token, PasswordResetRequest, PasswordResetConfirm
from app.crud.user import get_user_by_email, create_user, get_user_by_username
from app.core.security import verify_password, create_access_token, get_password_hash, create_password_reset_token, verify_password_reset_token
from app.services.email import send_reset_email, send_registration_email, send_account_created_email
from app.services.redis_otp import save_otp_registration,get_otp_registration, delete_otp_registration
from app.utils.otp import generate_otp

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/start-registration")
def start_registration(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(400, "Email already registered")
    if get_user_by_username(db, user.username):
        raise HTTPException(400, "Username already taken")

    otp = generate_otp()
    hashed_pw = get_password_hash(user.password)

    save_otp_registration(user.email, user.username, hashed_pw, otp)
    send_registration_email(user.email, otp)

    return {"msg": "OTP sent to email"}

@router.post("/verify-otp")
def verify_otp(email: str, otp: str, timezone: str, db: Session = Depends(get_db)):
    reg = get_otp_registration(email)
    if not reg or reg["otp"] != otp:
        raise HTTPException(400, "Invalid or expired OTP")

    user = User(
        email=email,
        username=reg["username"],
        hashed_password=reg["hashed_password"],
        timezone=timezone
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    delete_otp_registration(email)
    send_account_created_email(email)

    token = create_access_token({"sub": email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    user = create_user(db, user_in)
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

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