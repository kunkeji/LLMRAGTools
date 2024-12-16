"""
邮件标签模型
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseDBModel
from app.models.user import User

class EmailTag(BaseDBModel):
    """邮件标签模型"""
    __tablename__ = "email_tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(50))
    color: Mapped[str] = mapped_column(String(20), default="#1890ff")
    description: Mapped[Optional[str]] = mapped_column(String(200))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(None)

    # 关联关系
    user: Mapped[Optional[User]] = relationship("User", back_populates="email_tags")
    emails: Mapped[List["Email"]] = relationship(
        "Email",
        secondary="email_tag_relations",
        back_populates="tags",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<EmailTag {self.name}>"

class EmailTagRelation(BaseDBModel):
    """邮件标签关联模型"""
    __tablename__ = "email_tag_relations"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email_id: Mapped[int] = mapped_column(Integer, ForeignKey("emails.id", ondelete="CASCADE"))
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("email_tags.id", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"<EmailTagRelation email_id={self.email_id} tag_id={self.tag_id}>" 