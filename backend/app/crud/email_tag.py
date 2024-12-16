"""
邮件标签的CRUD操作
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.crud.base import CRUDBase
from app.models.email_tag import EmailTag, EmailTagRelation
from app.schemas.email_tag import EmailTagCreate, EmailTagUpdate

class CRUDEmailTag(CRUDBase[EmailTag, EmailTagCreate, EmailTagUpdate]):
    def get_by_name(
        self,
        db: Session,
        *,
        user_id: Optional[int],
        name: str
    ) -> Optional[EmailTag]:
        """通过名称获取标签"""
        return db.query(self.model).filter(
            and_(
                self.model.user_id == user_id,
                self.model.name == name,
                self.model.deleted_at.is_(None)
            )
        ).first()
    
    def get_system_tags(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[EmailTag]:
        """获取系统标签"""
        return db.query(self.model).filter(
            and_(
                self.model.is_system == True,
                self.model.deleted_at.is_(None)
            )
        ).order_by(
            self.model.sort_order.asc(),
            self.model.id.asc()
        ).offset(skip).limit(limit).all()
    
    def get_user_tags(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[EmailTag]:
        """获取用户标签"""
        return db.query(self.model).filter(
            and_(
                self.model.user_id == user_id,
                self.model.deleted_at.is_(None)
            )
        ).order_by(
            self.model.sort_order.asc(),
            self.model.id.asc()
        ).offset(skip).limit(limit).all()
    
    def get_all_available_tags(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[EmailTag]:
        """获取所有可用标签（系统标签 + 用户标签）"""
        return db.query(self.model).filter(
            and_(
                or_(
                    self.model.is_system == True,
                    self.model.user_id == user_id
                ),
                self.model.deleted_at.is_(None)
            )
        ).order_by(
            self.model.sort_order.asc(),
            self.model.id.asc()
        ).offset(skip).limit(limit).all()
    
    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: EmailTagCreate,
        user_id: int
    ) -> EmailTag:
        """创建用户标签"""
        db_obj = EmailTag(
            user_id=user_id,
            **obj_in.dict()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_tag_stats(
        self,
        db: Session,
        *,
        user_id: Optional[int] = None
    ) -> Dict[int, int]:
        """获取标签使用统计"""
        query = db.query(
            EmailTagRelation.tag_id,
            func.count(EmailTagRelation.email_id).label('email_count')
        ).group_by(EmailTagRelation.tag_id)
        
        if user_id:
            # 只统计用户自己的标签
            query = query.join(EmailTag).filter(
                or_(
                    EmailTag.is_system == True,
                    EmailTag.user_id == user_id
                )
            )
        
        return {
            row.tag_id: row.email_count
            for row in query.all()
        }
    
    def add_email_tag(
        self,
        db: Session,
        *,
        email_id: int,
        tag_id: int
    ) -> EmailTagRelation:
        """为邮件添加标签"""
        db_obj = EmailTagRelation(
            email_id=email_id,
            tag_id=tag_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove_email_tag(
        self,
        db: Session,
        *,
        email_id: int,
        tag_id: int
    ) -> None:
        """移除邮件标签"""
        db.query(EmailTagRelation).filter(
            and_(
                EmailTagRelation.email_id == email_id,
                EmailTagRelation.tag_id == tag_id
            )
        ).delete()
        db.commit()

crud_email_tag = CRUDEmailTag(EmailTag) 