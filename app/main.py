from fastapi import FastAPI
from app.api.v1 import auth, admin

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
