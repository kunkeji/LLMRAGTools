"""
邮件标签模型
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseDBModel

class EmailTag(BaseDBModel):
    """邮件标签模型"""
    __tablename__ = "email_tags"
    
    # 基本信息
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="标签名称"
    )
    color: Mapped[str] = mapped_column(
        String(7),
        nullable=False,
        comment="标签颜色(HEX)"
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True,
        comment="标签描述"
    )
    
    # 用户关联
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="用户ID"
    )
    action_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="标签动作名称"
    )
    
    # 排序
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="排序顺序"
    )
    
    # 时间信息
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="删除时间"
    )
    
    # 关联关系
    user = relationship("User", back_populates="email_tags")
    emails = relationship(
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
    
    email_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("emails.id", ondelete="CASCADE"),
        nullable=False,
        comment="邮件ID"
    )
    tag_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("email_tags.id", ondelete="CASCADE"),
        nullable=False,
        comment="标签ID"
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        comment="删除时间"
    )
    
    def __repr__(self) -> str:
        return f"<EmailTagRelation {self.email_id}-{self.tag_id}>" 