from fastapi import APIRouter
from app.api.v1.admin.endpoints import auth, users, llm

router = APIRouter()

# 管理员认证相关路由
router.include_router(
    auth.router,
    prefix="/auth",  # 将认证相关接口放在 /api/admin/auth 下
    tags=["管理认证"]
)

# 用户管理相关路由
router.include_router(
    users.router,
    tags=["管理后台"]
)

# LLM模型管理相关路由
router.include_router(
    llm.router,
    prefix="/llm",  # 将LLM相关接口放在 /api/admin/llm 下
    tags=["LLM管理"]
) 