from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class EmailAttachmentBase(BaseModel):
    """邮件附件基础模型"""
    filename: str
    content_type: str
    size: int
    is_inline: bool = False
    content_id: Optional[str] = None

class EmailAttachmentCreate(EmailAttachmentBase):
    """创建邮件附件模型"""
    email_id: int
    storage_path: str

class EmailAttachmentUpdate(EmailAttachmentBase):
    """更新邮件附件模型"""
    pass

class EmailAttachment(EmailAttachmentBase):
    """邮件附件返回模型"""
    id: int
    email_id: int
    storage_path: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmailBase(BaseModel):
    """邮件基础模型"""
    message_id: str
    subject: Optional[str] = None
    from_address: EmailStr
    from_name: Optional[str] = None
    to_address: List[EmailStr]
    cc_address: Optional[List[EmailStr]] = None
    bcc_address: Optional[List[EmailStr]] = None
    reply_to: Optional[List[EmailStr]] = None
    date: datetime
    content_type: str
    content: Optional[str] = None
    has_attachments: bool = False
    size: int = 0
    is_read: bool = False
    is_flagged: bool = False
    folder: str = "INBOX"
    importance: int = 0
    in_reply_to: Optional[str] = None
    references: Optional[List[str]] = None

class EmailCreate(EmailBase):
    """创建邮件模型"""
    account_id: int
    raw_content: Optional[str] = None

class EmailUpdate(BaseModel):
    """更新邮件模型"""
    is_read: Optional[bool] = None
    is_flagged: Optional[bool] = None
    folder: Optional[str] = None
    importance: Optional[int] = None

class Email(EmailBase):
    """邮件返回模型"""
    id: int
    account_id: int
    created_at: datetime
    updated_at: datetime
    attachments: List[EmailAttachment] = []

    class Config:
        from_attributes = True

class EmailSyncLogBase(BaseModel):
    """邮件同步日志基础模型"""
    account_id: int
    start_time: datetime
    status: str
    sync_type: str = "INCREMENT"

class EmailSyncLogCreate(EmailSyncLogBase):
    """创建邮件同步日志模型"""
    pass

class EmailSyncLogUpdate(BaseModel):
    """更新邮件同步日志模型"""
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    total_emails: Optional[int] = None
    new_emails: Optional[int] = None
    updated_emails: Optional[int] = None
    deleted_emails: Optional[int] = None
    error_message: Optional[str] = None

class EmailSyncLog(EmailSyncLogBase):
    """邮件同步日志返回模型"""
    id: int
    end_time: Optional[datetime] = None
    total_emails: int = 0
    new_emails: int = 0
    updated_emails: int = 0
    deleted_emails: int = 0
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True