from fastapi import APIRouter

from app.api.v1.user.endpoints.auth import router as user_auth_router
from app.api.v1.admin.endpoints.auth import router as admin_auth_router
from app.api.v1.admin.router import router as admin_router

api_router = APIRouter()

# User routes
api_router.include_router(user_auth_router, prefix="/user", tags=["user"])

# Admin routes
api_router.include_router(admin_auth_router, prefix="/admin/auth", tags=["admin"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])