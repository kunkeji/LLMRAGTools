from fastapi import APIRouter
from app.api.v1.user.endpoints import auth, password

router = APIRouter()

# 认证相关路由
router.include_router(auth.router, tags=["auth"])

# 密码相关路由
router.include_router(
    password.router,
    prefix="/password",
    tags=["password"]
) 