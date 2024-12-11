"""
API路由配置
"""
from fastapi import APIRouter
from app.api.v1.user import router as user_router
from app.api.v1.admin import router as admin_router

api_router = APIRouter()

# 用户相关路由
api_router.include_router(
    user_router.router,
    prefix="/user",
    tags=["用户"]
)

# 管理员相关路由
api_router.include_router(
    admin_router.router,
    prefix="/admin",
    tags=["管理员"]
)