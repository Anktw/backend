from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.user import User
from app.db.session import SessionLocal
from app.schemas.user import Token, PasswordResetRequest, PasswordResetConfirm, StartRegistrationRequest, VerifyOtpRequest, LoginRequest, ResendOtpRequest
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
def start_registration(payload: StartRegistrationRequest, db: Session = Depends(get_db)):
    email = payload.email.lower()
    username = payload.username.lower()

    if get_user_by_email(db, email):
        raise HTTPException(400, "Email already registered")
    if get_user_by_username(db, username):
        raise HTTPException(400, "Username already taken")

    otp = generate_otp()
    hashed_pw = get_password_hash(payload.password)

    save_otp_registration(email, username, hashed_pw, otp)
    #send_registration_email(email, otp)

    return {"msg": "OTP sent to email"}

@router.post("/verify-otp")
def verify_otp(payload: VerifyOtpRequest, db: Session = Depends(get_db)):
    email = payload.email.lower()
    reg = get_otp_registration(email)

    if not reg or reg["otp"] != payload.otp:
        raise HTTPException(400, "Invalid or expired OTP")

    user = User(
        email=email,
        username=reg["username"],
        hashed_password=reg["hashed_password"],
        timezone=payload.timezone
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    delete_otp_registration(email)
    send_account_created_email(email)

    token = create_access_token({
    "sub": email,
    "name": user.username if user.username else email,
})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/resend-otp")
def resend_otp(payload: ResendOtpRequest):
    email = payload.email.lower()

    reg = get_otp_registration(email)
    if not reg:
        raise HTTPException(400, "No pending registration found for this email")

    new_otp = generate_otp()
    save_otp_registration(email, reg["username"], reg["hashed_password"], new_otp)
    send_registration_email(email, new_otp)

    return {"msg": "A new OTP has been sent to your email."}


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(
            (User.email == payload.username_or_email.lower()) |
            (User.username == payload.username_or_email.lower())
        )
        .first()
    )

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token }


@router.post("/request-password-reset")
def request_password_reset(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(
            (User.email == payload.email_or_username.lower()) |
            (User.username == payload.email_or_username.lower())
        )
        .first()
    )
    if user:
        reset_token = create_password_reset_token(user.email)
        send_reset_email(user.email, reset_token)

    return {"msg": "If your account exists, a password reset email has been sent."}



@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    email = verify_password_reset_token(data.token)
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    return {"msg": "Password updated successfully"}


