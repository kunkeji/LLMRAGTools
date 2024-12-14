from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.crud.base import CRUDBase
from app.models.email import Email, EmailAttachment, EmailSyncLog
from app.schemas.email import EmailCreate, EmailUpdate, EmailAttachmentCreate, EmailAttachmentUpdate, EmailSyncLogCreate, EmailSyncLogUpdate

class CRUDEmail(CRUDBase[Email, EmailCreate, EmailUpdate]):
    """邮件CRUD操作类"""
    
    def get_by_message_id(self, db: Session, *, account_id: int, message_id: str) -> Optional[Email]:
        """根据message_id获取邮件"""
        return db.query(self.model).filter(
            and_(
                self.model.account_id == account_id,
                self.model.message_id == message_id
            )
        ).first()
    
    def get_multi_by_account(
        self,
        db: Session,
        *,
        account_id: int,
        folder: Optional[str] = None,
        is_read: Optional[bool] = None,
        is_flagged: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
        order_by: str = "date",
        order_desc: bool = True
    ) -> List[Email]:
        """获取账户的邮件列表"""
        query = db.query(self.model).filter(self.model.account_id == account_id)
        
        if folder:
            query = query.filter(self.model.folder == folder)
        if is_read is not None:
            query = query.filter(self.model.is_read == is_read)
        if is_flagged is not None:
            query = query.filter(self.model.is_flagged == is_flagged)
            
        # 排序
        if order_desc:
            query = query.order_by(desc(getattr(self.model, order_by)))
        else:
            query = query.order_by(getattr(self.model, order_by))
            
        return query.offset(skip).limit(limit).all()
    
    def get_unread_count(self, db: Session, *, account_id: int, folder: Optional[str] = None) -> int:
        """获取未读邮件数量"""
        query = db.query(self.model).filter(
            and_(
                self.model.account_id == account_id,
                self.model.is_read == False
            )
        )
        if folder:
            query = query.filter(self.model.folder == folder)
        return query.count()
    
    def mark_as_read(self, db: Session, *, email_id: int, is_read: bool = True) -> Optional[Email]:
        """标记邮件为已读/未读"""
        email = self.get(db, id=email_id)
        if email:
            email.is_read = is_read
            db.commit()
            db.refresh(email)
        return email
    
    def mark_as_flagged(self, db: Session, *, email_id: int, is_flagged: bool = True) -> Optional[Email]:
        """标记邮件为重要/取消重要"""
        email = self.get(db, id=email_id)
        if email:
            email.is_flagged = is_flagged
            db.commit()
            db.refresh(email)
        return email
    
    def move_to_folder(self, db: Session, *, email_id: int, folder: str) -> Optional[Email]:
        """移动邮件到指定文件夹"""
        email = self.get(db, id=email_id)
        if email:
            email.folder = folder
            db.commit()
            db.refresh(email)
        return email

class CRUDEmailAttachment(CRUDBase[EmailAttachment, EmailAttachmentCreate, EmailAttachmentUpdate]):
    """邮件附件CRUD操作类"""
    
    def get_multi_by_email(self, db: Session, *, email_id: int) -> List[EmailAttachment]:
        """获取邮件的所有附件"""
        return db.query(self.model).filter(self.model.email_id == email_id).all()

class CRUDEmailSyncLog(CRUDBase[EmailSyncLog, EmailSyncLogCreate, EmailSyncLogUpdate]):
    """邮件同步日志CRUD操作类"""
    
    def get_latest_by_account(self, db: Session, *, account_id: int) -> Optional[EmailSyncLog]:
        """获取账户最新的同步日志"""
        return db.query(self.model).filter(
            self.model.account_id == account_id
        ).order_by(desc(self.model.start_time)).first()
    
    def get_running_by_account(self, db: Session, *, account_id: int) -> Optional[EmailSyncLog]:
        """获取账户正在运行的同步任务"""
        return db.query(self.model).filter(
            and_(
                self.model.account_id == account_id,
                self.model.status == "RUNNING"
            )
        ).first()
    
    def update_sync_stats(
        self,
        db: Session,
        *,
        sync_id: int,
        total_emails: Optional[int] = None,
        new_emails: Optional[int] = None,
        updated_emails: Optional[int] = None,
        deleted_emails: Optional[int] = None
    ) -> Optional[EmailSyncLog]:
        """更新同步统计信息"""
        sync_log = self.get(db, id=sync_id)
        if sync_log:
            if total_emails is not None:
                sync_log.total_emails = total_emails
            if new_emails is not None:
                sync_log.new_emails = new_emails
            if updated_emails is not None:
                sync_log.updated_emails = updated_emails
            if deleted_emails is not None:
                sync_log.deleted_emails = deleted_emails
            db.commit()
            db.refresh(sync_log)
        return sync_log

email = CRUDEmail(Email)
email_attachment = CRUDEmailAttachment(EmailAttachment)
email_sync_log = CRUDEmailSyncLog(EmailSyncLog)