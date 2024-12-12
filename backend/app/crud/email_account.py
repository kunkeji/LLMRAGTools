"""
邮箱账户的CRUD操作
"""
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.email_account import EmailAccount, SyncStatus
from app.schemas.email_account import EmailAccountCreate, EmailAccountUpdate
from app.utils.email import test_smtp_connection, test_imap_connection

class CRUDEmailAccount(CRUDBase[EmailAccount, EmailAccountCreate, EmailAccountUpdate]):
    def get_by_email(
        self,
        db: Session,
        *,
        user_id: int,
        email: str
    ) -> Optional[EmailAccount]:
        """通过邮箱地址获取账户"""
        return db.query(EmailAccount).filter(
            and_(
                EmailAccount.user_id == user_id,
                EmailAccount.email_address == email
            )
        ).first()
    
    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[EmailAccount]:
        """获取用户的所有邮箱账户"""
        return db.query(EmailAccount).filter(
            EmailAccount.user_id == user_id
        ).offset(skip).limit(limit).all()
    
    def get_default_account(
        self,
        db: Session,
        *,
        user_id: int
    ) -> Optional[EmailAccount]:
        """获取用户的默认邮箱账户"""
        return db.query(EmailAccount).filter(
            and_(
                EmailAccount.user_id == user_id,
                EmailAccount.is_default == True
            )
        ).first()
    
    def get_next_account(
        self,
        db: Session,
        *,
        user_id: int,
        current_id: int
    ) -> Optional[EmailAccount]:
        """获取下一个可用的邮箱账户"""
        return db.query(EmailAccount).filter(
            and_(
                EmailAccount.user_id == user_id,
                EmailAccount.id != current_id,
                EmailAccount.is_active == True
            )
        ).first()
    
    def clear_default_status(
        self,
        db: Session,
        *,
        user_id: int
    ) -> None:
        """清除用户所有邮箱账户的默认状态"""
        db.query(EmailAccount).filter(
            and_(
                EmailAccount.user_id == user_id,
                EmailAccount.is_default == True
            )
        ).update({"is_default": False})
        db.commit()
    
    def create_with_user(
        self,
        db: Session,
        *,
        obj_in: EmailAccountCreate,
        user_id: int
    ) -> EmailAccount:
        """创建邮箱账户"""
        db_obj = EmailAccount(
            user_id=user_id,
            **obj_in.model_dump(exclude_unset=True)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_sync_status(
        self,
        db: Session,
        *,
        db_obj: EmailAccount,
        status: SyncStatus,
        error: Optional[str] = None
    ) -> EmailAccount:
        """更新同步状态"""
        update_data = {
            "sync_status": status,
            "last_sync_time": datetime.now(),
            "sync_error": error
        }
        
        if status == SyncStatus.SUCCESS:
            # 计算下次同步时间
            update_data["next_sync_time"] = datetime.now().timestamp() + (db_obj.sync_interval * 60)
            update_data["sync_error"] = None
        
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=update_data
        )
    
    def update_email_stats(
        self,
        db: Session,
        *,
        db_obj: EmailAccount,
        total_emails: int,
        unread_emails: int,
        last_email_time: Optional[datetime] = None
    ) -> EmailAccount:
        """更新邮件统计信息"""
        update_data = {
            "total_emails": total_emails,
            "unread_emails": unread_emails
        }
        if last_email_time:
            update_data["last_email_time"] = last_email_time
        
        return super().update(
            db,
            db_obj=db_obj,
            obj_in=update_data
        )
    
    async def test_connection(
        self,
        db: Session,
        account: EmailAccount
    ) -> bool:
        """
        测试邮箱账户连接
        
        Args:
            db: 数据库会话
            account: 邮箱账户对象
        
        Returns:
            bool: 是否测试成功
        """
        # 测试SMTP连接
        smtp_success, smtp_error = await test_smtp_connection(
            host=account.smtp_host,
            port=account.smtp_port,
            username=account.email_address,
            password=account.auth_token,
            use_ssl=account.use_ssl,
            use_tls=account.use_tls
        )
        
        # 更新SMTP测试结果
        account.smtp_last_test_time = datetime.utcnow()
        account.smtp_test_result = smtp_success
        account.smtp_test_error = smtp_error if not smtp_success else None
        
        # 测试IMAP连接
        imap_success, imap_error = await test_imap_connection(
            host=account.imap_host,
            port=account.imap_port,
            username=account.email_address,
            password=account.auth_token,
            use_ssl=account.use_ssl
        )
        
        # 更新IMAP测试结果
        account.imap_last_test_time = datetime.utcnow()
        account.imap_test_result = imap_success
        account.imap_test_error = imap_error if not imap_success else None
        
        # 保存测试结果
        db.add(account)
        db.commit()
        db.refresh(account)
        
        # 返回总体测试结果
        return smtp_success and imap_success
    
    def sync_emails(
        self,
        db: Session,
        db_obj: EmailAccount
    ) -> bool:
        """同步邮件
        TODO: 实现具体的邮件同步逻辑
        """
        try:
            # 更新状态为同步中
            self.update_sync_status(
                db,
                db_obj=db_obj,
                status=SyncStatus.SYNCING
            )
            
            # 实现邮件同步逻辑
            
            # 更新同步状态和统计信息
            self.update_sync_status(
                db,
                db_obj=db_obj,
                status=SyncStatus.SUCCESS
            )
            return True
        except Exception as e:
            self.update_sync_status(
                db,
                db_obj=db_obj,
                status=SyncStatus.FAILED,
                error=str(e)
            )
            return False

crud_email_account = CRUDEmailAccount(EmailAccount) 