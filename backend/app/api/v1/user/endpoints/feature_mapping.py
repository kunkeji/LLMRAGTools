"""
LLM功能映射接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.deps.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.llm_feature import LLMFeature, FeatureType
from app.models.llm_feature_mapping import LLMFeatureMapping
from app.crud.llm_feature_mapping import crud_feature_mapping
from app.schemas.response import response_success
from app.schemas.llm_feature_mapping import (
    LLMFeatureRead,
    LLMFeatureMappingCreate,
    LLMFeatureMappingUpdate,
    LLMFeatureMappingRead
)

router = APIRouter()

@router.get("/features", response_model=dict)
async def get_features(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取所有可用的LLM功能列表"""
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
                llm_model_id=mapping_in.llm_model_id,
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