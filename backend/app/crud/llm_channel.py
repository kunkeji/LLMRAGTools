"""
LLM渠道的CRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.llm_channel import LLMChannel
from app.schemas.llm_channel import LLMChannelCreate, LLMChannelUpdate

class CRUDLLMChannel(CRUDBase[LLMChannel, LLMChannelCreate, LLMChannelUpdate]):
    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: LLMChannelCreate,
        user_id: int
    ) -> LLMChannel:
        """创建用户的渠道"""
        db_obj = LLMChannel(
            user_id=user_id,
            channel_name=obj_in.channel_name,
            model_type=obj_in.model_type,
            model=obj_in.model,
            api_key=obj_in.api_key,
            proxy_url=obj_in.proxy_url
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[LLMChannel]:
        """获取用户的所有渠道"""
        return db.query(LLMChannel).filter(
            LLMChannel.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_name(
        self,
        db: Session,
        *,
        user_id: int,
        channel_name: str
    ) -> Optional[LLMChannel]:
        """通过渠道名称获取用户的渠道"""
        return db.query(LLMChannel).filter(
            LLMChannel.user_id == user_id,
            LLMChannel.channel_name == channel_name
        ).first()
    
    def search_channels(
        self,
        db: Session,
        *,
        user_id: int,
        keyword: Optional[str] = None,
        model_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[LLMChannel]:
        """搜索用户的渠道"""
        query = db.query(LLMChannel).filter(LLMChannel.user_id == user_id)
        
        if keyword:
            query = query.filter(
                or_(
                    LLMChannel.channel_name.ilike(f"%{keyword}%"),
                    LLMChannel.model_type.ilike(f"%{keyword}%"),
                    LLMChannel.model.ilike(f"%{keyword}%")
                )
            )
        
        if model_type:
            query = query.filter(LLMChannel.model_type == model_type)
        
        return query.offset(skip).limit(limit).all()

crud_llm_channel = CRUDLLMChannel(LLMChannel) 