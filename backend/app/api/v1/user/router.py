from fastapi import APIRouter
from app.api.v1.user.endpoints import auth, password, profile

router = APIRouter()

# 认证相关路由（登录、注册、验证码等）
router.include_router(
    auth.router,
    tags=["用户认证"],
    prefix=""  # 保持在 /api/user/ 下
)

# 密码相关路由（重置密码等）
router.include_router(
    password.router,
    prefix="/password",
    tags=["用户认证"]
)

# 个人信息相关路由
router.include_router(
    profile.router,
    prefix="/profile",
    tags=["用户管理"]
) 