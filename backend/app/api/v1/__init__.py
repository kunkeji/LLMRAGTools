from fastapi import APIRouter

# 导入路由
from app.api.v1.admin.router import router as admin_router
from app.api.v1.admin.endpoints.auth import router as admin_auth_router
from app.api.v1.user.router import router as user_router
from app.api.v1.user.endpoints.auth import router as user_auth_router

# 创建主路由
api_router = APIRouter()

# 包含子路由
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(admin_auth_router, prefix="/admin/auth", tags=["admin-auth"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(user_auth_router, prefix="/user/auth", tags=["user-auth"])