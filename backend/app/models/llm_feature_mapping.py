"""
LLM功能映射模型
"""
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base_model import BaseDBModel

class LLMFeatureMapping(BaseDBModel):
    """LLM功能映射"""
    __tablename__ = "llm_feature_mappings"

    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="映射ID"
    )
    
    user_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    
    llm_model_id: int = Column(
        Integer,
        ForeignKey("llm_channels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="渠道ID"
    )
    
    feature_type: str = Column(
        String(50),
        ForeignKey("llm_features.feature_type", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="功能类型"
    )
    
    prompt_template: str = Column(
        Text,
        nullable=True,
        comment="自定义提示词模板"
    )
    
    last_used_at: DateTime = Column(
        DateTime,
        nullable=True,
        comment="最后使用时间"
    )
    
    use_count: int = Column(
        Integer,
        default=0,
        comment="使用次数"
    )
    
    # 关联关系
    user = relationship(
        "User",
        back_populates="feature_mappings",
        lazy="select"
    )
    
    channel = relationship(
        "LLMChannel",
        back_populates="feature_mappings",
        lazy="select"
    )
    
    feature = relationship(
        "LLMFeature",
        back_populates="feature_mappings",
        lazy="select"
    )
    
    def __repr__(self) -> str:
        return f"<LLMFeatureMapping {self.feature_type}>"
    
    def update_usage(self) -> None:
        """更新使用统计"""
        self.last_used_at = datetime.now()
        self.use_count += 1