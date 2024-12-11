"""
LLM模型管理接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.deps.auth import get_current_admin, get_db
from app.crud.llm_model import crud_llm_model
from app.models.admin import Admin
from app.schemas.llm_model import LLMModel, LLMModelCreate, LLMModelUpdate
from app.schemas.response import response_success
from app.utils.logger import logger_instance
from app.models.log import LogType

router = APIRouter()

@router.post("/models", summary="创建LLM模型")
def create_model(
    *,
    db: Session = Depends(get_db),
    model_in: LLMModelCreate,
    current_admin: Admin = Depends(get_current_admin)
) -> dict:
    """创建新的LLM模型"""
    logger_instance.info(
        message=f"创建LLM模型: {model_in.name}",
        module="admin.llm",
        function="create_model",
        type=LogType.OPERATION,
        user_id=current_admin.id,
        username=current_admin.username
    )
    
    # 检查名称是否已存在
    if crud_llm_model.get_by_name(db, name=model_in.name):
        raise HTTPException(
            status_code=400,
            detail="该模型名称已存在"
        )
    
    # 检查映射名称是否已存在
    if crud_llm_model.get_by_mapping_name(db, mapping_name=model_in.mapping_name):
        raise HTTPException(
            status_code=400,
            detail="该映射名称已存在"
        )
    
    model = crud_llm_model.create(db, obj_in=model_in)
    return response_success(data=model)

@router.get("/models", summary="获取LLM模型列表")
def get_models(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin),
    skip: int = 0,
    limit: int = 100,
    keyword: str = None,
) -> dict:
    """获取LLM模型列表"""
    models = crud_llm_model.search_models(
        db,
        keyword=keyword,
        skip=skip,
        limit=limit
    )
    return response_success(data=models)

@router.get("/models/{model_id}", summary="获取LLM模型详情")
def get_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
) -> dict:
    """获取指定LLM模型的详细信息"""
    model = crud_llm_model.get(db, id=model_id)
    if not model:
        raise HTTPException(
            status_code=404,
            detail="模型不存在"
        )
    return response_success(data=model)

@router.put("/models/{model_id}", summary="更新LLM模型")
def update_model(
    *,
    db: Session = Depends(get_db),
    model_id: int,
    model_in: LLMModelUpdate,
    current_admin: Admin = Depends(get_current_admin)
) -> dict:
    """更新LLM模型信息"""
    logger_instance.info(
        message=f"更新LLM模型: {model_id}",
        module="admin.llm",
        function="update_model",
        type=LogType.OPERATION,
        user_id=current_admin.id,
        username=current_admin.username
    )
    
    model = crud_llm_model.get(db, id=model_id)
    if not model:
        raise HTTPException(
            status_code=404,
            detail="模型不存在"
        )
    
    model = crud_llm_model.update(db, db_obj=model, obj_in=model_in)
    return response_success(data=model)

@router.delete("/models/{model_id}", summary="删除LLM模型")
def delete_model(
    *,
    db: Session = Depends(get_db),
    model_id: int,
    current_admin: Admin = Depends(get_current_admin)
) -> dict:
    """删除LLM模型"""
    logger_instance.info(
        message=f"删除LLM模型: {model_id}",
        module="admin.llm",
        function="delete_model",
        type=LogType.OPERATION,
        user_id=current_admin.id,
        username=current_admin.username
    )
    
    model = crud_llm_model.get(db, id=model_id)
    if not model:
        raise HTTPException(
            status_code=404,
            detail="模型不存在"
        )
    
    model = crud_llm_model.remove(db, id=model_id)
    return response_success(message="删除成功") 