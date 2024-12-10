from fastapi import APIRouter
from app.api.v1.user.router import router as user_router
from app.api.v1.admin.router import router as admin_router

api_router = APIRouter()

# 注册用户路由（不在这里设置 tags，由子路由设置）
api_router.include_router(user_router, prefix="/user")

# 注册管理员路由（不在这里设置 tags，由子路由设置）
api_router.include_router(admin_router, prefix="/admin")