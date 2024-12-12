"""
邮箱提供商的CRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.email_provider import EmailProvider
from app.schemas.email_provider import EmailProviderCreate, EmailProviderUpdate

class CRUDEmailProvider(CRUDBase[EmailProvider, EmailProviderCreate, EmailProviderUpdate]):
    def get_by_name(
        self,
        db: Session,
        *,
        name: str
    ) -> Optional[EmailProvider]:
        """通过名称获取提供商"""
        return db.query(EmailProvider).filter(EmailProvider.name == name).first()
    
    def get_by_domain(
        self,
        db: Session,
        *,
        domain: str
    ) -> Optional[EmailProvider]:
        """通过域名后缀获取提供商"""
        if not domain.startswith('@'):
            domain = '@' + domain
        return db.query(EmailProvider).filter(EmailProvider.domain_suffix == domain).first()
    
    def get_active_providers(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[EmailProvider]:
        """获取所有启用的提供商"""
        return db.query(EmailProvider).filter(
            EmailProvider.is_active == True
        ).order_by(
            EmailProvider.sort_order.asc(),
            EmailProvider.id.asc()
        ).offset(skip).limit(limit).all()
    
    def search_providers(
        self,
        db: Session,
        *,
        keyword: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[EmailProvider]:
        """搜索提供商"""
        query = db.query(EmailProvider)
        
        if keyword:
            query = query.filter(
                or_(
                    EmailProvider.name.ilike(f"%{keyword}%"),
                    EmailProvider.domain_suffix.ilike(f"%{keyword}%"),
                    EmailProvider.description.ilike(f"%{keyword}%")
                )
            )
        
        if is_active is not None:
            query = query.filter(EmailProvider.is_active == is_active)
        
        return query.order_by(
            EmailProvider.sort_order.asc(),
            EmailProvider.id.asc()
        ).offset(skip).limit(limit).all()

crud_email_provider = CRUDEmailProvider(EmailProvider) 