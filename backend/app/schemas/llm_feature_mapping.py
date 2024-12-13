"""
LLM功能映射相关的Schema定义
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.base import BaseSchema
from app.models.llm_feature import FeatureType

class LLMFeatureBase(BaseModel):
    """功能定义基础Schema"""
    feature_type: FeatureType = Field(..., description="功能类型")
    name: str = Field(..., description="功能名称")
    description: Optional[str] = Field(None, description="功能描述")
    default_prompt: str = Field(..., description="默认提示词模板")

class LLMFeatureRead(LLMFeatureBase):
    """功能定义读取Schema"""
    class Config:
        from_attributes = True

class LLMFeatureMappingBase(BaseModel):
    """功能映射基础Schema"""
    llm_model_id: int = Field(..., description="LLM模型ID")
    feature_type: FeatureType = Field(..., description="功能类型")
    prompt_template: Optional[str] = Field(None, description="自定义提示词模板")

class LLMFeatureMappingCreate(LLMFeatureMappingBase):
    """功能映射创建Schema"""
    pass

class LLMFeatureMappingUpdate(BaseModel):
    """功能映射更新Schema"""
    llm_model_id: Optional[int] = Field(None, description="LLM模型ID")
    prompt_template: Optional[str] = Field(None, description="自定义提示词模板")

class LLMFeatureMappingRead(LLMFeatureMappingBase, BaseSchema):
    """功能映射读取Schema"""
    id: int
    user_id: int
    last_used_at: Optional[datetime] = None
    use_count: int = 0
    
    class Config:
        from_attributes = True