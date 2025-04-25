from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.core.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from app.db.models.user import User
from app.db.session import SessionLocal
from app.schemas.user import Token, PasswordResetRequest, PasswordResetConfirm, StartRegistrationRequest, VerifyOtpRequest, LoginRequest, ResendOtpRequest
from app.crud.user import get_user_by_email, get_user_by_username
from app.core.security import verify_password, create_access_token, get_password_hash, create_password_reset_token, verify_password_reset_token, create_refresh_token
from app.services.email import send_reset_email, send_registration_email, send_account_created_email, send_password_changed_email
from app.services.redis_otp import save_otp_registration,get_otp_registration, delete_otp_registration, save_otp_reset, get_otp_reset, delete_otp_reset
from app.utils.otp import generate_otp
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.requests import Request as StarletteRequest



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
    send_registration_email(email, otp)

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

    access_token = create_access_token({
        "sub": email,
        "name": user.username if user.username else email,
    })

    refresh_token = create_refresh_token({
        "sub": email
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

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
    refresh_token = create_refresh_token({"sub": user.email})
    
    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
}


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
        email = user.email.lower()
        otp = generate_otp()
        save_otp_reset(email=email, otp=otp)
        send_reset_email(email, otp)

    return {"msg": "If your account exists, a password reset email has been sent."}


@router.post("/verify-reset-otp")
def verify_reset_otp(payload: VerifyOtpRequest):
    email = payload.email.lower()
    reg = get_otp_reset(email)

    if not reg or reg["otp"] != payload.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    delete_otp_reset(email)
    reset_token = create_password_reset_token(email)
    return {"reset_token": reset_token}


@router.post("/resend-reset-otp")
def resend_reset_otp(payload: ResendOtpRequest):
    email = payload.email.lower()

    reg = get_otp_reset(email)
    if not reg:
        raise HTTPException(400, "No pending password reset found for this email")

    new_otp = generate_otp()
    save_otp_reset(email=email, otp=new_otp)
    send_reset_email(email, new_otp)

    return {"msg": "A new OTP has been sent to your email."}


@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    email = verify_password_reset_token(data.token)
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(data.new_password)
    db.commit()
    send_password_changed_email(user.email)
    return {"msg": "Password updated successfully"}



@router.post("/refresh", response_model=Token)
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    access_token = create_access_token({"sub": email})
    return {"access_token": access_token}


# Google and Github OAuth config
config = Config(environ={
    'GOOGLE_CLIENT_ID': settings.GOOGLE_CLIENT_ID,
    'GOOGLE_CLIENT_SECRET': settings.GOOGLE_CLIENT_SECRET,
    'SECRET_KEY': settings.SECRET_KEY,
    'GITHUB_CLIENT_ID': getattr(settings, 'GITHUB_CLIENT_ID', ''),
    'GITHUB_CLIENT_SECRET': getattr(settings, 'GITHUB_CLIENT_SECRET', ''),
})
oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)
oauth.register(
    name='github',
    client_id=getattr(settings, 'GITHUB_CLIENT_ID', ''),
    client_secret=getattr(settings, 'GITHUB_CLIENT_SECRET', ''),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'}
)

@router.get('/login/google')
async def login_google(request: StarletteRequest):
    redirect_uri = str(request.url_for('auth_google_callback'))
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/login/github')
async def login_github(request: StarletteRequest):
    redirect_uri = str(request.url_for('auth_github_callback'))
    return await oauth.github.authorize_redirect(request, redirect_uri)

@router.get('/google/callback')
def auth_google_callback(request: StarletteRequest, db: Session = Depends(get_db)):
    token = oauth.google.authorize_access_token(request)
    user_info = oauth.google.parse_id_token(request, token)
    email = user_info['email'].lower()
    user = get_user_by_email(db, email)
    if not user:
        user = User(email=email, username=email.split('@')[0], hashed_password='')
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token = create_access_token({'sub': user.email})
    refresh_token = create_refresh_token({'sub': user.email})

    response = RedirectResponse(url='/user/dashboard')
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'response': response
    }

@router.get('/github/callback')
async def auth_github_callback(request: StarletteRequest, db: Session = Depends(get_db)):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get('user', token=token)
    profile = resp.json()
    email = profile.get('email')
    if not email:
        # fetch primary email if not public
        emails_resp = await oauth.github.get('user/emails', token=token)
        emails = emails_resp.json()
        email = next((e['email'] for e in emails if e.get('primary')), None)
    if not email:
        raise HTTPException(400, 'Unable to retrieve email from GitHub')
    email = email.lower()
    user = get_user_by_email(db, email)
    if not user:
        user = User(email=email, username=profile.get('login', email.split('@')[0]), hashed_password='')
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token = create_access_token({'sub': user.email})
    refresh_token = create_refresh_token({'sub': user.email})
    response = RedirectResponse(url='/user/dashboard')
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer',
        'response': response
    }
