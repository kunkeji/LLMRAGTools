from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.v1.deps.auth import get_current_super_admin, get_db
from app.crud import crud_user
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.admin import Admin
from app.schemas.response import response_success

router = APIRouter()

@router.get("/users", summary="获取用户列表")
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: Admin = Depends(get_current_super_admin),
):
    """
    获取所有用户列表（需要超级管理员权限）
    """
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return response_success(
        data=users,
        message="获取成功"
    )

@router.post("/users", summary="创建用户")
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_admin: Admin = Depends(get_current_super_admin),
):
    """
    创建新用户（需要超级管理员权限）
    """
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册",
        )
    user = crud_user.create(db, obj_in=user_in)
    return response_success(
        data=user,
        message="用户创建成功"
    )

@router.get("/users/{user_id}", summary="获取用户信息")
def read_user(
    user_id: int,
    current_admin: Admin = Depends(get_current_super_admin),
    db: Session = Depends(get_db),
):
    """
    通过ID获取用户信息（需要超级管理员权限）
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    return response_success(
        data=user,
        message="获取成功"
    )

@router.put("/users/{user_id}", summary="更新用户信息")
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_admin: Admin = Depends(get_current_super_admin),
):
    """
    更新用户信息（需要超级管理员权限）
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    return response_success(
        data=user,
        message="更新成功"
    )

@router.delete("/users/{user_id}", summary="删除用户")
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_admin: Admin = Depends(get_current_super_admin),
):
    """
    删除用户（软删除，需要超级管理员权限）
    """
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    user = crud_user.soft_delete(db, id=user_id)
    return response_success(
        data=user,
        message="删除成功"
    )
