from fastapi import APIRouter, Response, Depends, HTTPException
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import httpx
import secrets

from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
)
from app.db.models.user import User
from app.crud.user import get_user_by_email
from app.api.deps import get_db

router = APIRouter()

# ---------- GOOGLE AUTH ----------
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
    return RedirectResponse(url, status_code=302)

@router.get("/auth/callback/google")
async def callback_google(code: str, db: Session = Depends(get_db)):
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
        access_token = tokens.get("access_token")
        if not access_token:
            raise HTTPException(400, detail="Google token exchange failed")

        userinfo_resp = await client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
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
    refresh_token = create_refresh_token({"sub": user.email})

    # ✅ Redirect to frontend page to finalize session cookie
    redirect_url = (
        f"{settings.FRONTEND_URL}/auth/social/callback"
        f"?access_token={jwt_token}&refresh_token={refresh_token}"
    )
    return RedirectResponse(url=redirect_url, status_code=302)

# ---------- GITHUB AUTH ----------
@router.get("/auth/github")
async def auth_github():
    redirect_uri = f"{settings.BACKEND_URL}/api/auth/callback/github"
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": "read:user user:email",
    }
    url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url, status_code=302)

@router.get("/auth/callback/github")
async def callback_github(code: str, db: Session = Depends(get_db)):
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(token_url, headers=headers, data={
            "code": code,
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
        })

        tokens = token_resp.json()
        access_token = tokens.get("access_token")
        if not access_token:
            raise HTTPException(400, detail="GitHub token exchange failed")

        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        userinfo = user_resp.json()

        email_resp = await client.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        emails = email_resp.json()
        email = next((e["email"] for e in emails if e.get("primary") and e.get("verified")), None)

    if not email:
        raise HTTPException(400, detail="Could not retrieve a verified email from GitHub")

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
    refresh_token = create_refresh_token({"sub": user.email})

    redirect_url = (
        f"{settings.FRONTEND_URL}/auth/social/callback"
        f"?access_token={jwt_token}&refresh_token={refresh_token}"
    )
    return RedirectResponse(url=redirect_url, status_code=302)
