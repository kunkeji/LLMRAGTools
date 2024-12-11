"""
LLM模型渠道管理模型
"""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base_model import BaseDBModel

class LLMChannel(BaseDBModel):
    """LLM模型渠道信息"""
    __tablename__ = "llm_channels"

    user_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    channel_name: str = Column(
        String(100),
        nullable=False,
        comment="渠道名称"
    )
    model_type: str = Column(
        String(50),
        nullable=False,
        comment="模型类型"
    )
    model: str = Column(
        String(50),
        nullable=False,
        comment="具体模型"
    )
    api_key: str = Column(
        String(500),
        nullable=False,
        comment="API密钥"
    )
    proxy_url: str = Column(
        String(200),
        nullable=True,
        comment="代理地址(可选)"
    )

    # 关联用户
    user = relationship("User", back_populates="llm_channels")

    def __repr__(self) -> str:
        return f"<LLMChannel {self.channel_name} ({self.model_type}/{self.model})>" 