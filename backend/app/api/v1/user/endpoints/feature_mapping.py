"""
LLM功能映射接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Form, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.v1.deps.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.llm_feature import LLMFeature, FeatureType
from app.crud.llm_feature_mapping import crud_feature_mapping
from app.schemas.response import response_success
from app.schemas.llm_feature_mapping import (
    LLMFeatureMappingCreate,
    LLMFeatureMappingUpdate,
)
from app.features.feature_interface import FeatureInterface
from app.core.exceptions import FeatureNotConfiguredError

router = APIRouter()

class MessageRequest(BaseModel):
    """消息请求模型"""
    message: str

@router.get("/features", response_model=dict)
async def get_features(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """��取所有可用的LLM功能列表"""
    features = db.query(LLMFeature).all()
    return response_success(data=features)

@router.get("/mappings", response_model=dict)
async def get_user_mappings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的功能映射配置"""
    mappings = crud_feature_mapping.get_multi_by_user(
        db=db,
        user_id=current_user.id
    )
    return response_success(data=mappings)

@router.post("/mappings/save", response_model=dict)
async def save_mapping(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    mapping_in: LLMFeatureMappingCreate
):
    """保存功能映射(新增或更新)"""
    # 检查是否已存在相同功能类型的映射
    existing = crud_feature_mapping.get_by_feature_type(
        db=db,
        user_id=current_user.id,
        feature_type=mapping_in.feature_type
    )
    
    if existing:
        # 如果存在则更新
        mapping = crud_feature_mapping.update(
            db=db,
            db_obj=existing,
            obj_in=LLMFeatureMappingUpdate(
                channel_id=mapping_in.channel_id,
                prompt_template=mapping_in.prompt_template
            )
        )
    else:
        # 如果不存在则创建
        mapping = crud_feature_mapping.create_with_user(
            db=db,
            obj_in=mapping_in,
            user_id=current_user.id
        )
    
    return response_success(data=mapping) 

@router.post("/execute/{feature_type}", response_class=StreamingResponse)
async def execute_feature(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    feature_type: FeatureType,
    request: MessageRequest
):
    """执行特定功能
    
    Args:
        feature_type: 功能类型
        request: 包含用户消息的请求体
    """
    try:
        # 使用功能映射接口执行功能
        stream = FeatureInterface.execute_feature_stream(
            db=db,
            user_id=current_user.id,
            feature_type=feature_type,
            message=request.message
        )
        
        return StreamingResponse(
            stream,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
        
    except FeatureNotConfiguredError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) 