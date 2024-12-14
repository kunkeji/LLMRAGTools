"""
LLM功能映射的CRUD操作
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.llm_feature_mapping import LLMFeatureMapping
from app.models.llm_feature import FeatureType
from app.schemas.llm_feature_mapping import LLMFeatureMappingCreate, LLMFeatureMappingUpdate

class CRUDFeatureMapping(CRUDBase[LLMFeatureMapping, LLMFeatureMappingCreate, LLMFeatureMappingUpdate]):
    """功能映射CRUD操作类"""
    
    @staticmethod
    def get_by_feature_type(
        db: Session,
        *,
        user_id: int,
        feature_type: FeatureType
    ) -> Optional[LLMFeatureMapping]:
        """根据功能类型获取映射"""
        return db.query(LLMFeatureMapping).filter(
            LLMFeatureMapping.user_id == user_id,
            LLMFeatureMapping.feature_type == feature_type
        ).first()
    
    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[LLMFeatureMapping]:
        """获取用户的所有功能映射"""
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: LLMFeatureMappingCreate,
        user_id: int
    ) -> LLMFeatureMapping:
        """创建用户的功能映射"""
        db_obj = LLMFeatureMapping(
            user_id=user_id,
            **obj_in.dict()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_feature_mapping = CRUDFeatureMapping(LLMFeatureMapping) 