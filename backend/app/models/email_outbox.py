from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class EmailOutbox(Base):
    __tablename__ = "email_outbox"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("email_accounts.id", ondelete="CASCADE"), nullable=False)
    reply_to_email_id = Column(Integer, ForeignKey("emails.id", ondelete="SET NULL"), nullable=True)
    reply_type = Column(Enum("pre_reply", "auto_reply", "manual_reply", "quick_reply", name="reply_type"), nullable=True)
    
    recipients = Column(Text, nullable=False)
    cc = Column(Text, nullable=True)
    bcc = Column(Text, nullable=True)
    subject = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    content_type = Column(String(50), nullable=False, default="text/html")
    
    attachments = Column(Text, nullable=True)
    status = Column(Enum("draft", "pending", "sent", "failed", name="email_status"), nullable=False, default="draft")
    send_time = Column(DateTime, nullable=True)
    error_message = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, nullable=True)
    
    # 关联关系
    account = relationship("EmailAccount", back_populates="outbox_emails")
    reply_to_email = relationship("Email", back_populates="replies") 