"""
邮件标签管理接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_user, get_db
from app.models.user import User
from app.crud.email_tag import crud_email_tag
from app.schemas.email_tag import (
    EmailTag,
    EmailTagCreate,
    EmailTagUpdate,
    EmailTagWithStats
)
from app.schemas.response import response_success

router = APIRouter()

@router.get("/tags", summary="获取所有可用标签")
def get_all_tags(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    include_stats: bool = False
) -> dict:
    """
    获取所有可用标签（系统标签 + 用户标签）
    
    - **skip**: 跳过记录数
    - **limit**: 返回记录数
    - **include_stats**: 是否包含统计信息
    """
    tags = crud_email_tag.get_all_available_tags(
        db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )
    
    if include_stats:
        # 获取标签使用统计
        stats = crud_email_tag.get_tag_stats(db, user_id=current_user.id)
        tags_with_stats = []
        for tag in tags:
            # 使用Pydantic模型的model_validate方法转换
            tag_model = EmailTagWithStats.model_validate(tag)
            tag_model.email_count = stats.get(tag.id, 0)
            tags_with_stats.append(tag_model)
        return response_success(data=tags_with_stats)
    
    # 使用Pydantic模型的model_validate方法转换
    tag_list = [EmailTag.model_validate(tag) for tag in tags]
    return response_success(data=tag_list)

@router.post("/tags", summary="创建标签")
def create_tag(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tag_in: EmailTagCreate
) -> dict:
    """
    创建新标签
    
    - 不能创建与系统标签或已有标签同名的标签
    """
    # 检查是否存在同名标签
    if crud_email_tag.get_by_name(db, user_id=current_user.id, name=tag_in.name):
        raise HTTPException(
            status_code=400,
            detail="标签名称已存在"
        )
    
    tag = crud_email_tag.create_with_user(
        db,
        obj_in=tag_in,
        user_id=current_user.id
    )
    return response_success(data=tag)

@router.put("/tags/{tag_id}", summary="更新标签")
def update_tag(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tag_id: int,
    tag_in: EmailTagUpdate
) -> dict:
    """
    更新标签信息
    
    - 只能更新用户自己创建的标签
    - 不能修改系统标签
    """
    tag = crud_email_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail="标签不存在"
        )
    
    # 检查权限
    if tag.is_system:
        raise HTTPException(
            status_code=403,
            detail="不能修改系统标签"
        )
    if tag.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="只能修改自己创建的标签"
        )
    
    # 如果要更新名称，检查是否存在同名标签
    if tag_in.name and tag_in.name != tag.name:
        if crud_email_tag.get_by_name(db, user_id=current_user.id, name=tag_in.name):
            raise HTTPException(
                status_code=400,
                detail="标签名称已存在"
            )
    
    tag = crud_email_tag.update(db, db_obj=tag, obj_in=tag_in)
    return response_success(data=tag)

@router.delete("/tags/{tag_id}", summary="删除标签")
def delete_tag(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    tag_id: int
) -> dict:
    """
    删除标签
    
    - 只能删除用户自己创建的标签
    - 不能删除系统标签
    """
    tag = crud_email_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail="标签不存在"
        )
    
    # 检查权限
    if tag.is_system:
        raise HTTPException(
            status_code=403,
            detail="不能删除系统标签"
        )
    if tag.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="只能删除自己创建的标签"
        )
    
    crud_email_tag.remove(db, id=tag_id)
    return response_success(message="标签删除成功")

@router.post("/emails/{email_id}/tags/{tag_id}", summary="添加邮件标签")
def add_email_tag(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    email_id: int,
    tag_id: int
) -> dict:
    """
    为邮件添加标签
    """
    # 检查标签是否存在且可用
    tag = crud_email_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail="标签不存在"
        )
    
    # 检查是否是系统标签或用户自己的标签
    if not tag.is_system and tag.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="只能使用系统标签或自己创建的标签"
        )
    
    crud_email_tag.add_email_tag(db, email_id=email_id, tag_id=tag_id)
    return response_success(message="标签添加成功")

@router.delete("/emails/{email_id}/tags/{tag_id}", summary="移除邮件标签")
def remove_email_tag(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    email_id: int,
    tag_id: int
) -> dict:
    """
    移除邮件标签
    """
    # 检查标签是否存在
    tag = crud_email_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail="标签不存在"
        )
    
    crud_email_tag.remove_email_tag(db, email_id=email_id, tag_id=tag_id)
    return response_success(message="标签移除成功") 