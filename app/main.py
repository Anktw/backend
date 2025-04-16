from fastapi import FastAPI
from app.api.v1 import auth, admin
from app.core.startup import init_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    init_db()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
