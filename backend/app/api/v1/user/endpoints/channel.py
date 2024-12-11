"""
用户LLM渠道管理接口
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_user, get_db
from app.crud.llm_channel import crud_llm_channel
from app.models.user import User
from app.schemas.llm_channel import LLMChannel, LLMChannelCreate, LLMChannelUpdate
from app.schemas.response import response_success
from app.utils.logger import logger_instance
from app.models.log import LogType

router = APIRouter()

@router.post("/", summary="创建LLM渠道")
def create_channel(
    *,
    db: Session = Depends(get_db),
    channel_in: LLMChannelCreate,
    current_user: User = Depends(get_current_user)
) -> dict:
    """创建新的LLM渠道"""
    logger_instance.info(
        message=f"创建LLM渠道: {channel_in.channel_name}",
        module="user.channel",
        function="create_channel",
        type=LogType.OPERATION,
        user_id=current_user.id,
        username=current_user.username
    )
    
    # 检查渠道名称是否已存在
    if crud_llm_channel.get_by_name(
        db,
        user_id=current_user.id,
        channel_name=channel_in.channel_name
    ):
        raise HTTPException(
            status_code=400,
            detail="该渠道名称已存在"
        )
    
    channel = crud_llm_channel.create_with_user(
        db,
        obj_in=channel_in,
        user_id=current_user.id
    )
    return response_success(data=channel)

@router.get("/", summary="获取LLM渠道列表")
def get_channels(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    keyword: Optional[str] = None,
    model_type: Optional[str] = None
) -> dict:
    """获取用户的LLM渠道列表"""
    channels = crud_llm_channel.search_channels(
        db,
        user_id=current_user.id,
        keyword=keyword,
        model_type=model_type,
        skip=skip,
        limit=limit
    )
    return response_success(data=channels)

@router.get("/{channel_id}", summary="获取LLM渠道详情")
def get_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """获取指定LLM渠道的详细信息"""
    channel = crud_llm_channel.get(db, id=channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="渠道不存在"
        )
    return response_success(data=channel)

@router.put("/{channel_id}", summary="更新LLM渠道")
def update_channel(
    *,
    db: Session = Depends(get_db),
    channel_id: int,
    channel_in: LLMChannelUpdate,
    current_user: User = Depends(get_current_user)
) -> dict:
    """更新LLM渠道信息"""
    logger_instance.info(
        message=f"更新LLM渠道: {channel_id}",
        module="user.channel",
        function="update_channel",
        type=LogType.OPERATION,
        user_id=current_user.id,
        username=current_user.username
    )
    
    channel = crud_llm_channel.get(db, id=channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="渠道不存在"
        )
    
    # 如果更新渠道名称，检查是否与其他渠道重名
    if channel_in.channel_name and channel_in.channel_name != channel.channel_name:
        if crud_llm_channel.get_by_name(
            db,
            user_id=current_user.id,
            channel_name=channel_in.channel_name
        ):
            raise HTTPException(
                status_code=400,
                detail="该渠道名称已存在"
            )
    
    channel = crud_llm_channel.update(db, db_obj=channel, obj_in=channel_in)
    return response_success(data=channel)

@router.delete("/{channel_id}", summary="删除LLM渠道")
def delete_channel(
    *,
    db: Session = Depends(get_db),
    channel_id: int,
    current_user: User = Depends(get_current_user)
) -> dict:
    """删除LLM渠道"""
    logger_instance.info(
        message=f"删除LLM渠道: {channel_id}",
        module="user.channel",
        function="delete_channel",
        type=LogType.OPERATION,
        user_id=current_user.id,
        username=current_user.username
    )
    
    channel = crud_llm_channel.get(db, id=channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="渠道不存在"
        )
    
    channel = crud_llm_channel.remove(db, id=channel_id)
    return response_success(message="删除成功") 