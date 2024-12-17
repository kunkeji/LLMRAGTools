from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseDBModel
from app.models.email_account import EmailAccount

class Email(BaseDBModel):
    """邮件模型"""
    __tablename__ = "emails"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("email_accounts.id", ondelete="CASCADE"))
    message_id: Mapped[str] = mapped_column(String(255))
    subject: Mapped[Optional[str]] = mapped_column(String(500))
    from_address: Mapped[str] = mapped_column(String(255))
    from_name: Mapped[Optional[str]] = mapped_column(String(100))
    to_address: Mapped[List[str]] = mapped_column(JSON)
    cc_address: Mapped[Optional[List[str]]] = mapped_column(JSON)
    bcc_address: Mapped[Optional[List[str]]] = mapped_column(JSON)
    reply_to: Mapped[Optional[List[str]]] = mapped_column(JSON)
    date: Mapped[datetime] = mapped_column(DateTime)
    content_type: Mapped[str] = mapped_column(String(50))
    content: Mapped[Optional[str]] = mapped_column(String)
    raw_content: Mapped[Optional[str]] = mapped_column(String)
    has_attachments: Mapped[bool] = mapped_column(Boolean, default=False)
    size: Mapped[int] = mapped_column(Integer, default=0)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    is_flagged: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    folder: Mapped[str] = mapped_column(String(50), default="INBOX")
    importance: Mapped[int] = mapped_column(Integer, default=0)
    in_reply_to: Mapped[Optional[str]] = mapped_column(String(255))
    references: Mapped[Optional[List[str]]] = mapped_column(JSON)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # 关联关系
    account: Mapped[EmailAccount] = relationship("EmailAccount", back_populates="emails")
    attachments: Mapped[List["EmailAttachment"]] = relationship("EmailAttachment", back_populates="email", cascade="all, delete-orphan")
    tags: Mapped[List["EmailTag"]] = relationship(
        "EmailTag",
        secondary="email_tag_relations",
        back_populates="emails",
        lazy="selectin"
    )
    replies: Mapped[List["EmailOutbox"]] = relationship("EmailOutbox", back_populates="reply_to_email")

    def __repr__(self) -> str:
        return f"<Email {self.subject}>"

class EmailAttachment(BaseDBModel):
    """邮件附件模型"""
    __tablename__ = "email_attachments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email_id: Mapped[int] = mapped_column(Integer, ForeignKey("emails.id", ondelete="CASCADE"))
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(100))
    size: Mapped[int] = mapped_column(Integer)
    storage_path: Mapped[str] = mapped_column(String(500))
    content_id: Mapped[Optional[str]] = mapped_column(String(255))
    is_inline: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # 关联关系
    email: Mapped[Email] = relationship("Email", back_populates="attachments")

class EmailSyncLog(BaseDBModel):
    """邮件同步日志模型"""
    __tablename__ = "email_sync_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("email_accounts.id", ondelete="CASCADE"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(Enum("RUNNING", "COMPLETED", "FAILED", "CANCELLED", "TIMEOUT", name="sync_status"))
    total_emails: Mapped[int] = mapped_column(Integer, default=0)
    new_emails: Mapped[int] = mapped_column(Integer, default=0)
    updated_emails: Mapped[int] = mapped_column(Integer, default=0)
    deleted_emails: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(String(500))
    sync_type: Mapped[str] = mapped_column(Enum("FULL", "INCREMENT", name="sync_type"), default="INCREMENT")

    # 关联关系
    account: Mapped[EmailAccount] = relationship("EmailAccount", back_populates="sync_logs")