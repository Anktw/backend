from fastapi import APIRouter, Request, Response, Depends, status
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import httpx
from app.core.config import settings
from app.api.deps import get_db
from app.db.models.user import User
from app.crud.user import get_user_by_email
from app.core.security import create_access_token
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
import secrets

router = APIRouter()

# GOOGLE AUTH
@router.get("/auth/google")
async def auth_google():
    redirect_uri = f"{settings.BACKEND_URL}/api/auth/callback/google"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/auth/callback/google")
async def callback_google(code: str, response: Response, db: Session = Depends(get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    redirect_uri = f"{settings.BACKEND_URL}/api/auth/callback/google"

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(token_url, data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
        })

        tokens = token_resp.json()
        access_token_google = tokens.get("access_token")

        userinfo_resp = await client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token_google}"}
        )
        userinfo = userinfo_resp.json()

    email = userinfo["email"]
    username = userinfo.get("name") or email.split("@")[0]

    user = get_user_by_email(db, email)
    if not user:
        user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(secrets.token_urlsafe(16)),
            timezone="UTC",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = create_access_token({"sub": user.email})
    response = RedirectResponse(url=f"{settings.FRONTEND_URL}/user/dashboard")
    response.set_cookie("session", jwt_token, httponly=True, secure=True)
    return response


# GITHUB AUTH
@router.get("/auth/github")
async def auth_github():
    redirect_uri = f"{settings.BACKEND_URL}/api/auth/callback/github"
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": "read:user user:email",
    }
    url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/auth/callback/github")
async def callback_github(code: str, response: Response, db: Session = Depends(get_db)):
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(token_url, headers=headers, data={
            "code": code,
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
        })

        tokens = token_resp.json()
        access_token_github = tokens["access_token"]

        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token_github}"}
        )
        userinfo = user_resp.json()

        email_resp = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token_github}"}
        )
        emails = email_resp.json()
        email = next((e["email"] for e in emails if e.get("primary") and e.get("verified")), None)

    if not email:
        return {"error": "Could not verify email"}

    username = userinfo["login"]

    user = get_user_by_email(db, email)
    if not user:
        user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(secrets.token_urlsafe(16)),
            timezone="UTC",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = create_access_token({"sub": user.email})
    response = RedirectResponse(url=f"{settings.FRONTEND_URL}/user/dashboard")
    response.set_cookie("session", jwt_token, httponly=True, secure=True)
    return response
