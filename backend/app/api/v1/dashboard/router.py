from fastapi import APIRouter, Depends
from app.api.v1.dashboard.service import DashboardService
from app.dependencies.current_user import get_current_user
from app.api.v1.auth.schemas import UserResponse

router = APIRouter(prefix="/dashboard", tags=["User Dashboard"])

@router.get("/summary")
async def get_dashboard_summary(current_user: UserResponse = Depends(get_current_user)):
    return await DashboardService.get_user_dashboard_summary(current_user.id)
