"""
LLM渠道管理接口
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time

from app.api.v1.deps.auth import get_current_active_user, get_db
from app.crud.llm_channel import crud_llm_channel
from app.models.user import User
from app.schemas.llm_channel import LLMChannel, LLMChannelCreate, LLMChannelUpdate
from app.schemas.response import response_success
from app.utils.logger import logger_instance
from app.models.log import LogType
from app.utils.llm import LLMClient

router = APIRouter()

@router.post("", summary="创建LLM渠道")
def create_channel(
    *,
    db: Session = Depends(get_db),
    channel_in: LLMChannelCreate,
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """创建新的LLM渠道"""
    # 检查渠道名称是否已存在
    if crud_llm_channel.get_by_name(
        db, user_id=current_user.id, channel_name=channel_in.channel_name
    ):
        raise HTTPException(
            status_code=400,
            detail="该渠道名称已存在"
        )
    
    channel = crud_llm_channel.create_with_user(
        db, obj_in=channel_in, user_id=current_user.id
    )
    return response_success(data=channel)

@router.get("", summary="获取LLM渠道列表")
def get_channels(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    keyword: Optional[str] = None,
    model_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
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
    current_user: User = Depends(get_current_active_user)
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
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """更新LLM渠道信息"""
    channel = crud_llm_channel.get(db, id=channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="渠道不存在"
        )
    
    # 如果更新渠道名称，检查是否与其他渠道重名
    if channel_in.channel_name and channel_in.channel_name != channel.channel_name:
        if crud_llm_channel.get_by_name(
            db, user_id=current_user.id, channel_name=channel_in.channel_name
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
    current_user: User = Depends(get_current_active_user)
) -> dict:
    """删除LLM渠道"""
    channel = crud_llm_channel.get(db, id=channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="渠道不存在"
        )
    
    crud_llm_channel.remove(db, id=channel_id)
    return response_success(message="删除成功")

@router.post("/{channel_id}/test", summary="测试LLM渠道")
async def test_channel(
    *,
    db: Session = Depends(get_db),
    channel_id: int,
    current_user: User = Depends(get_current_active_user)
) -> dict:
    # 获取渠道信息
    channel = crud_llm_channel.get(db, id=channel_id)
    if not channel or channel.user_id != current_user.id:
        raise HTTPException(
            status_code=404,
            detail="渠道不存在"
        )
    
    try:
        # 记录开始测试日志
        logger_instance.info(
            message=f"开始测试渠道: {channel.channel_name}",
            module="channel.test",
            function="test_channel",
            type=LogType.OPERATION,
            user_id=current_user.id,
            username=current_user.username
        )
        
        # 准备测试参数
        test_prompt = "你好，这是一条测试消息。请回复'1'。"
        test_message = "你好"
        
        # 记录开始时间
        start_time = time.perf_counter()

        # 获取流式响应
        stream = LLMClient.generate_stream(
            prompt=test_prompt,
            message=test_message,
            api_key=channel.api_key,
            provider=channel.model_type,
            model=channel.model
        )

        # 获取第一个响应并计算时间
        first_token = None
        response_time = 0
        async for chunk in stream:
            # 计算响应时间（毫秒）
            response_time = int((time.perf_counter() - start_time) * 1000)
            first_token = chunk
            break

       
        
        # 更新渠道的响应时间统计
        channel.update_response_time(response_time)
        db.add(channel)
        db.commit()
        db.refresh(channel)
        
        # 准备测试结果
        test_result = {
            "success": True,
            "response_time": response_time,
            "first_token": first_token,
            "channel_info": {
                "id": channel.id,
                "name": channel.channel_name,
                "model_type": channel.model_type,
                "model": channel.model
            },
            "performance": {
                "last_response_time": channel.last_response_time,
                "avg_response_time": channel.avg_response_time,
                "min_response_time": channel.min_response_time,
                "max_response_time": channel.max_response_time,
                "test_count": channel.test_count,
                "last_test_time": channel.last_test_time
            }
        }
        
        # 记录测试成功日志
        logger_instance.info(
            message=f"渠道测试成功: {channel.channel_name}, 响应时间: {response_time}ms",
            module="channel.test",
            function="test_channel",
            type=LogType.OPERATION,
            user_id=current_user.id,
            username=current_user.username,
            details=test_result
        )
        
        return response_success(
            data=test_result,
            message="渠道测试成功"
        )
        
    except Exception as e:
        # 记录测试失败日志
        error_message = str(e)
        logger_instance.error(
            message=f"渠道测试失败: {channel.channel_name}, 错误: {error_message}",
            module="channel.test",
            function="test_channel",
            type=LogType.OPERATION,
            user_id=current_user.id,
            username=current_user.username,
            error_type=type(e).__name__,
            error_stack=error_message
        )
        
        raise HTTPException(
            status_code=400,
            detail=f"渠道测试失败: {error_message}"
        ) 