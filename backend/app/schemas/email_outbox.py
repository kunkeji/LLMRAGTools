from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class EmailOutboxBase(BaseModel):
    recipients: str
    cc: Optional[str] = None
    bcc: Optional[str] = None
    subject: Optional[str] = None
    content: str
    content_type: str = "text/html"
    attachments: Optional[str] = None

class EmailOutboxCreate(EmailOutboxBase):
    account_id: Optional[int] = None  # 可选,如果不传则使用默认账户
    reply_to_email_id: Optional[int] = None  # 可选,如果传入则表示是回复邮件
    reply_type: Optional[str] = None  # 回复类型

class EmailOutboxUpdate(EmailOutboxBase):
    status: Optional[str] = None
    error_message: Optional[str] = None
    send_time: Optional[datetime] = None

class EmailOutboxInDBBase(EmailOutboxBase):
    id: int
    account_id: int
    status: str
    reply_to_email_id: Optional[int]
    reply_type: Optional[str]
    send_time: Optional[datetime]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmailOutbox(EmailOutboxInDBBase):
    pass 