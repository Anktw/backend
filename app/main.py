import time
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.db.session import engine
from fastapi import FastAPI
from app.api.v1 import auth, admin, user, social_auth, lockin
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings

app = FastAPI()

@app.on_event("startup")
def wait_for_db():
    retries = 10
    while retries > 0:
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database is ready!")
            break
        except OperationalError:
            print("Database not ready, waiting...")
            time.sleep(2)
            retries -= 1
    else:
        raise Exception("Database connection failed after retries")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(user.router, prefix="/user", tags=["user"]) 
app.include_router(lockin.router, prefix="/lockin", tags=["lockin"])
app.include_router(social_auth.router, prefix="/api")
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)