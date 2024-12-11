"""
用户端LLM模型接口
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_db
from app.crud.llm_model import crud_llm_model
from app.schemas.response import response_success
from app.models.llm_model import ModelStatus
from app.schemas.llm_model import LLMModel

router = APIRouter()

@router.get("/models", summary="获取可用的LLM模型列表", response_model=dict)
def get_available_models(
    db: Session = Depends(get_db)
) -> dict:
    """
    获取所有可用的LLM模型列表
    
    返回:
    - 所有状态为ACTIVE且公开可用的模型列表
    """
    models = crud_llm_model.search_models(
        db,
        status=ModelStatus.ACTIVE,
        is_public=True
    )
    
    # 将模型对象转换为字典列表
    models_list = [
        {
            "id": model.id,
            "name": model.name,
            "mapping_name": model.mapping_name,
            "description": model.description
        }
        for model in models
    ]
    
    return response_success(data=models_list) 