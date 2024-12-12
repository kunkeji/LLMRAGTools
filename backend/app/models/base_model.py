from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer
from app.db.base_class import Base

class BaseDBModel(Base):
    """
    基础数据模型，提供通用字段
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True,
        autoincrement=True,
        comment="主键ID"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="更新时间"
    )
    deleted_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=True,
        comment="删除时间"
    )

    def soft_delete(self) -> None:
        """
        软删除
        """
        self.deleted_at = datetime.now()

    @property
    def is_deleted(self) -> bool:
        """
        是否已删除
        """
        return self.deleted_at is not None 