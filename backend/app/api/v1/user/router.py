"""
用户API路由配置
"""
from fastapi import APIRouter
from app.api.v1.user.endpoints import (
    auth,
    profile,
    password,
    llm,
    channel,
    email,
    document,
    feature_mapping
)

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

# LLM模型相关路由
router.include_router(
    llm.router,
    prefix="/llm",  # 将LLM相关接口放在 /api/user/llm 下
    tags=["LLM服务"]
)

# LLM渠道管理相关路由
router.include_router(
    channel.router,
    prefix="/channel",  # 将渠道管理接口放在 /api/user/channel 下
    tags=["渠道管理"]
)

# 邮箱提供商管理路由
router.include_router(
    email.router,
    prefix="/email",
    tags=["admin-email"]
)

# 文档管理路由
router.include_router(
    document.router,
    prefix="/documents",
    tags=["文档管理"]
)

router.include_router(
    feature_mapping.router,
    prefix="/feature-mappings",
    tags=["功能映射"]
) 