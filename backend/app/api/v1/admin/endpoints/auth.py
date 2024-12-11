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
from app.utils.logger import logger_instance
from app.models.log import LogType

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
    logger_instance.info(
        message=f"管理员登录请求: {form_data.username}",
        module="admin.auth",
        function="admin_login",
        type=LogType.SECURITY
    )
    
    try:
        admin = crud_admin.authenticate(
            db, username=form_data.username, password=form_data.password
        )
        if not admin:
            logger_instance.warning(
                message=f"管理员登录失败,用户名或密码错误: {form_data.username}",
                module="admin.auth",
                function="admin_login",
                type=LogType.SECURITY
            )
            raise HTTPException(status_code=400, detail="用户名或密码错误")
        elif not admin.is_active:
            logger_instance.warning(
                message=f"管理员登录失败,账号未激活: {form_data.username}",
                module="admin.auth",
                function="admin_login",
                type=LogType.SECURITY
            )
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
        
        logger_instance.info(
            message=f"管理员登录成功: {admin.username}",
            module="admin.auth",
            function="admin_login",
            type=LogType.SECURITY,
            user_id=admin.id,
            username=admin.username,
            role=admin.role
        )
        
        return response_success(
            data=token,
            message="登录成功"
        )
    
    except Exception as e:
        logger_instance.error(
            message=f"管理员登录失败: {str(e)}",
            module="admin.auth",
            function="admin_login",
            type=LogType.SECURITY,
            error_type=type(e).__name__,
            error_stack=str(e)
        )
        raise

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
    logger_instance.info(
        message=f"创建管理员请求: {admin_in.username}",
        module="admin.auth",
        function="create_admin",
        type=LogType.OPERATION,
        user_id=current_admin.id,
        username=current_admin.username
    )
    
    try:
        admin = crud_admin.get_by_email(db, email=admin_in.email)
        if admin:
            logger_instance.warning(
                message=f"创建管理员失败,邮箱已被注册: {admin_in.email}",
                module="admin.auth",
                function="create_admin",
                type=LogType.OPERATION
            )
            raise HTTPException(
                status_code=400,
                detail="该邮箱已被注册"
            )
        
        admin = crud_admin.get_by_username(db, username=admin_in.username)
        if admin:
            logger_instance.warning(
                message=f"创建管理员失败,用户名已被使用: {admin_in.username}",
                module="admin.auth",
                function="create_admin",
                type=LogType.OPERATION
            )
            raise HTTPException(
                status_code=400,
                detail="该用户名已被使用"
            )
        
        admin = crud_admin.create(db, obj_in=admin_in)
        logger_instance.info(
            message=f"管理员创建成功: {admin.username}",
            module="admin.auth",
            function="create_admin",
            type=LogType.OPERATION,
            user_id=current_admin.id,
            username=current_admin.username,
            target_admin_id=admin.id,
            target_admin_username=admin.username,
            target_admin_role=admin.role
        )
        
        return response_success(
            data=admin,
            message="管理员创建成功"
        )
    
    except Exception as e:
        logger_instance.error(
            message=f"创建管理员失败: {str(e)}",
            module="admin.auth",
            function="create_admin",
            type=LogType.OPERATION,
            error_type=type(e).__name__,
            error_stack=str(e),
            user_id=current_admin.id,
            username=current_admin.username
        )
        raise

@router.get("/me", summary="获取当前管理员信息")
def read_admin_me(
    current_admin: Admin = Depends(get_current_admin),
) -> Any:
    """
    获取当前登录管理员信息
    """
    logger_instance.info(
        message=f"获取管理员信息: {current_admin.username}",
        module="admin.auth",
        function="read_admin_me",
        type=LogType.OPERATION,
        user_id=current_admin.id,
        username=current_admin.username,
        role=current_admin.role
    )
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
    logger_instance.info(
        message="获取管理员列表",
        module="admin.auth",
        function="list_admins",
        type=LogType.OPERATION,
        user_id=current_admin.id,
        username=current_admin.username,
        details={"skip": skip, "limit": limit}
    )
    
    try:
        admins = crud_admin.get_multi(db, skip=skip, limit=limit)
        return response_success(
            data=admins,
            message="获取成功"
        )
    
    except Exception as e:
        logger_instance.error(
            message=f"获取管理员列表失败: {str(e)}",
            module="admin.auth",
            function="list_admins",
            type=LogType.OPERATION,
            error_type=type(e).__name__,
            error_stack=str(e),
            user_id=current_admin.id,
            username=current_admin.username
        )
        raise
 