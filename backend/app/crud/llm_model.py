"""
LLM模型的CRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.llm_model import LLMModel, ModelStatus
from app.schemas.llm_model import LLMModelCreate, LLMModelUpdate

class CRUDLLMModel(CRUDBase[LLMModel, LLMModelCreate, LLMModelUpdate]):
    def get_by_name(
        self,
        db: Session,
        *,
        name: str
    ) -> Optional[LLMModel]:
        """通过名称获取模型"""
        return db.query(LLMModel).filter(LLMModel.name == name).first()
    
    def get_by_mapping_name(
        self,
        db: Session,
        *,
        mapping_name: str
    ) -> Optional[LLMModel]:
        """通过映射名称获取模型"""
        return db.query(LLMModel).filter(LLMModel.mapping_name == mapping_name).first()
    
    def get_active_models(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[LLMModel]:
        """获取所有活跃的模型"""
        return db.query(LLMModel).filter(
            LLMModel.status == ModelStatus.ACTIVE
        ).offset(skip).limit(limit).all()
    
    def get_public_models(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[LLMModel]:
        """获取所有公开的模型"""
        return db.query(LLMModel).filter(
            LLMModel.is_public == True
        ).offset(skip).limit(limit).all()
    
    def search_models(
        self,
        db: Session,
        *,
        keyword: Optional[str] = None,
        status: Optional[ModelStatus] = None,
        is_public: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[LLMModel]:
        """搜索模型"""
        query = db.query(LLMModel)
        
        if keyword:
            query = query.filter(
                or_(
                    LLMModel.name.ilike(f"%{keyword}%"),
                    LLMModel.mapping_name.ilike(f"%{keyword}%"),
                    LLMModel.description.ilike(f"%{keyword}%")
                )
            )
        
        if status is not None:
            # 确保使用枚举值
            if isinstance(status, str):
                try:
                    status = ModelStatus[status.upper()]
                except KeyError:
                    raise ValueError(f"Invalid status value: {status}")
            query = query.filter(LLMModel.status == status)
        
        if is_public is not None:
            query = query.filter(LLMModel.is_public == is_public)
        
        return query.offset(skip).limit(limit).all()

crud_llm_model = CRUDLLMModel(LLMModel) 