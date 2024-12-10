from datetime import timedelta
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_admin, get_current_super_admin, get_db
from app.core.config import settings
from app.core.security import jwt
from app.crud import crud_admin
from app.models.admin import Admin
from app.schemas.token import Token
from app.schemas.admin import Admin as AdminSchema, AdminCreate
from app.schemas.response import response_success

router = APIRouter(tags=["管理认证"])

@router.post("/login", summary="管理员登录")
def admin_login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    管理员登录接口
    
    - **username**: 管理员用户名
    - **password**: 密码
    """
    admin = crud_admin.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not admin:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    elif not admin.is_active:
        raise HTTPException(status_code=400, detail="管理员账号未激活")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = {
        "access_token": jwt.create_access_token(
            subject=str(admin.id),
            token_type="admin",
            expires_delta=access_token_expires,
            extra_data={"role": admin.role}
        ),
        "token_type": "bearer",
    }
    
    return response_success(
        data=token,
        message="登录成功"
    )

@router.post("/create", summary="创建管理员")
def create_admin(
    *,
    db: Session = Depends(get_db),
    admin_in: AdminCreate,
    current_admin: Admin = Depends(get_current_super_admin)
) -> Any:
    """
    创建新管理员（需要超级管理员权限）
    
    - **username**: 用户名
    - **email**: 邮箱
    - **password**: 密码
    - **full_name**: 全名
    - **role**: 角色（admin/super_admin）
    - **phone_number**: 电话号码（可选）
    """
    admin = crud_admin.get_by_email(db, email=admin_in.email)
    if admin:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册"
        )
    
    admin = crud_admin.get_by_username(db, username=admin_in.username)
    if admin:
        raise HTTPException(
            status_code=400,
            detail="该用户名已被使用"
        )
    
    admin = crud_admin.create(db, obj_in=admin_in)
    return response_success(
        data=admin,
        message="管理员创建成功"
    )

@router.get("/me", summary="获取当前管理员信息")
def read_admin_me(
    current_admin: Admin = Depends(get_current_admin),
) -> Any:
    """
    获取当前登录管理员信息
    """
    return response_success(
        data=current_admin,
        message="获取成功"
    )

@router.get("/list", summary="管理员列表")
def list_admins(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_super_admin),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取管理员列表（需要超级管理员权限）
    
    - **skip**: 跳过记录数
    - **limit**: 返回记录数（默认100）
    """
    admins = crud_admin.get_multi(db, skip=skip, limit=limit)
    return response_success(
        data=admins,
        message="获取成功"
    ) 