from typing import Optional, List, Union, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.email_outbox import EmailOutbox
from app.models.email_account import EmailAccount
from app.models.email import Email
from app.schemas.email_outbox import EmailOutboxCreate, EmailOutboxUpdate
from app.utils.email import SMTPClient

class CRUDEmailOutbox(CRUDBase[EmailOutbox, EmailOutboxCreate, EmailOutboxUpdate]):
    def create_email(
        self,
        db: Session,
        *,
        obj_in: EmailOutboxCreate,
        user_id: int
    ) -> EmailOutbox:
        """
        创建待发送邮件
        如果指定了account_id则使用指定账户
        如果指定了reply_to_email_id则使用原邮件的账户
        否则使用用户默认邮箱账户
        """
        obj_in_data = jsonable_encoder(obj_in)
        
        # 确定发件账户
        account_id = obj_in.account_id
        if not account_id and obj_in.reply_to_email_id:
            # 如果是回���件,使用原邮件的账户
            original_email = db.query(Email).filter(Email.id == obj_in.reply_to_email_id).first()
            if original_email:
                account_id = original_email.account_id
                
        if not account_id:
            # 使用用户默认邮箱账户
            default_account = db.query(EmailAccount)\
                .filter(EmailAccount.user_id == user_id, EmailAccount.is_default == True)\
                .first()
            if default_account:
                account_id = default_account.id
            else:
                # 如果没有默认账户,使用用户的第一个邮箱账户
                first_account = db.query(EmailAccount)\
                    .filter(EmailAccount.user_id == user_id)\
                    .first()
                if first_account:
                    account_id = first_account.id
                    
        if not account_id:
            raise ValueError("No available email account found")
            
        obj_in_data["account_id"] = account_id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[EmailOutbox]:
        """获取用户的所有发送邮件，支持筛选"""
        query = db.query(self.model)\
            .join(EmailAccount)\
            .filter(EmailAccount.user_id == user_id)
            
        # 添加筛选条件
        if filters:
            if filters.get("status"):
                query = query.filter(self.model.status == filters["status"])
            if filters.get("reply_type"):
                query = query.filter(self.model.reply_type == filters["reply_type"])
            if filters.get("account_id"):
                query = query.filter(self.model.account_id == filters["account_id"])
            if filters.get("search"):
                search = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        self.model.subject.ilike(search),
                        self.model.recipients.ilike(search),
                        self.model.content.ilike(search)
                    )
                )
            if filters.get("start_date"):
                query = query.filter(self.model.created_at >= filters["start_date"])
            if filters.get("end_date"):
                query = query.filter(self.model.created_at <= filters["end_date"])
                
        # 添加排序
        query = query.order_by(self.model.created_at.desc())
        
        return query.offset(skip).limit(limit).all()
    
    def get_total_count(
        self,
        db: Session,
        *,
        user_id: int,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """获取符合条件的总记录数"""
        query = db.query(self.model)\
            .join(EmailAccount)\
            .filter(EmailAccount.user_id == user_id)
            
        # 添加筛选条件
        if filters:
            if filters.get("status"):
                query = query.filter(self.model.status == filters["status"])
            if filters.get("reply_type"):
                query = query.filter(self.model.reply_type == filters["reply_type"])
            if filters.get("account_id"):
                query = query.filter(self.model.account_id == filters["account_id"])
            if filters.get("search"):
                search = f"%{filters['search']}%"
                query = query.filter(
                    or_(
                        self.model.subject.ilike(search),
                        self.model.recipients.ilike(search),
                        self.model.content.ilike(search)
                    )
                )
            if filters.get("start_date"):
                query = query.filter(self.model.created_at >= filters["start_date"])
            if filters.get("end_date"):
                query = query.filter(self.model.created_at <= filters["end_date"])
                
        return query.count()
    
    def get_by_id_and_user(
        self,
        db: Session,
        *,
        email_id: int,
        user_id: int
    ) -> Optional[EmailOutbox]:
        """获取指定ID的邮件（需验证用户权限）"""
        return db.query(self.model)\
            .join(EmailAccount, self.model.account_id == EmailAccount.id)\
            .filter(
                self.model.id == email_id,
                EmailAccount.user_id == user_id
            ).first()
    
    def delete(
        self,
        db: Session,
        *,
        email_id: int,
        user_id: int
    ) -> bool:
        """删除邮件（硬删除）"""
        db_obj = self.get_by_id_and_user(db, email_id=email_id, user_id=user_id)
        if not db_obj:
            return False
            
        db.delete(db_obj)
        db.commit()
        return True
    
    async def resend_email(
        self,
        db: Session,
        *,
        id: int,
        user_id: int
    ) -> Optional[EmailOutbox]:
        """重新发送失败的邮件"""
        db_obj = self.get_by_id_and_user(db, id=id, user_id=user_id)
        if not db_obj:
            return None
            
        if db_obj.status == "sent":
            raise ValueError("Email already sent successfully")
            
        # 重置状态
        db_obj.status = "draft"
        db_obj.error_message = None
        db_obj.send_time = None
        db.commit()
        db.refresh(db_obj)
        
        # 重新发送
        return await self.send_email(db, email_id=id, user_id=user_id)
    
    async def send_email(
        self,
        db: Session,
        *,
        email_id: int,
        user_id: int
    ) -> EmailOutbox:
        """
        发送邮件
        1. 检查邮件是否存在且属于该用户
        2. 获取邮箱账户信息
        3. 调用发送邮件工具
        4. 更新邮件状态
        """
        # 获取邮件信息
        db_obj = db.query(self.model)\
            .join(EmailAccount)\
            .filter(
                self.model.id == email_id,
                EmailAccount.user_id == user_id
            ).first()
            
        if not db_obj:
            raise ValueError("Email not found or no permission")
            
        if db_obj.status == "sent":
            raise ValueError("Email already sent")
            
        try:
            smtp_client = SMTPClient(
                host=db_obj.account.smtp_host,
                port=db_obj.account.smtp_port,
                username=db_obj.account.email_address,
                password=db_obj.account.auth_token
            )
            
            # 拼接html
            db_obj.html_content = f"<html><body>{db_obj.content}</body></html>"
            
            try:
                # 调用发送邮件工具
                await smtp_client.send_email(
                    to_addresses=db_obj.recipients.split(","),
                    subject=db_obj.subject,
                    content=db_obj.html_content,
                    content_type=db_obj.content_type,
                    cc_addresses=db_obj.cc.split(",") if db_obj.cc else None,
                    bcc_addresses=db_obj.bcc.split(",") if db_obj.bcc else None,
                    from_name=db_obj.account.email_address
                )
                # 如果发送成功，即使有响应解析错误也标记为已发送
                db_obj.status = "sent"
                db_obj.send_time = datetime.now()
                db_obj.error_message = None  # 清除可能存在的错误信息
                db.commit()
                db.refresh(db_obj)
                return db_obj
                
            except Exception as e:
                error_str = str(e)
                # 检查是否是已知的非致命性错误
                if "Malformed SMTP response line" in error_str and db_obj.status != "failed":
                    # 如果是响应解析错误，且邮件状态不是失败，认为邮件已发送成功
                    db_obj.status = "sent"
                    db_obj.send_time = datetime.now()
                    db_obj.error_message = None
                    db.commit()
                    db.refresh(db_obj)
                    return db_obj
                else:
                    # 其他错误则标记为失败
                    db_obj.status = "failed"
                    db_obj.error_message = error_str
                    db.commit()
                    db.refresh(db_obj)
                    raise ValueError(f"Failed to send email: {error_str}")
                
        except Exception as e:
            # 连接SMTP服务器失败等其他错误
            db_obj.status = "failed"
            db_obj.error_message = str(e)
            db.commit()
            db.refresh(db_obj)
            raise ValueError(f"Failed to send email: {str(e)}")

email_outbox = CRUDEmailOutbox(EmailOutbox) 