"""
大语言模型相关的Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import Field, field_validator
from app.schemas.base import BaseSchema
from app.models.llm_model import ModelStatus

class LLMModelBase(BaseSchema):
    """LLM模型基础Schema"""
    name: str = Field(..., min_length=1, max_length=100, description="模型名称")
    mapping_name: str = Field(..., min_length=1, max_length=50, description="映射名称")
    status: ModelStatus = Field(default=ModelStatus.ACTIVE, description="模型状态")
    is_public: bool = Field(default=True, description="是否公开可用")
    description: Optional[str] = Field(None, max_length=500, description="模型描述")

    @field_validator('mapping_name')
    def validate_mapping_name(cls, v: str) -> str:
        """验证映射名称格式"""
        if not v.isalnum() and not all(c in '_-' for c in v if not c.isalnum()):
            raise ValueError('映射名称只能包含字母、数字、下划线和连字符')
        return v.lower()

class LLMModelCreate(LLMModelBase):
    """创建LLM模型"""
    pass

class LLMModelUpdate(BaseSchema):
    """更新LLM模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="模型名称")
    status: Optional[ModelStatus] = Field(None, description="模型状态")
    is_public: Optional[bool] = Field(None, description="是否公开可用")
    description: Optional[str] = Field(None, max_length=500, description="模型描述")

class LLMModelInDBBase(LLMModelBase):
    """数据库中的LLM模型基础信息"""
    id: int = Field(..., description="模型ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class LLMModel(LLMModelInDBBase):
    """API响应中的LLM模型信息"""
    pass

class LLMModelInDB(LLMModelInDBBase):
    """数据库中的完整LLM模型信息"""
    pass 