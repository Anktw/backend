from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_active_admin

router = APIRouter()

@router.get("/admin-only")
def admin_dashboard(current_user = Depends(get_current_active_admin)):
    return {"msg": f"Hello admin {current_user.email}"}
