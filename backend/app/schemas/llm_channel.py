"""
LLM渠道管理的Schema
"""
from typing import Optional
from pydantic import BaseModel, Field

class LLMChannelBase(BaseModel):
    """LLM渠道基础Schema"""
    channel_name: str = Field(..., description="渠道名称", max_length=100)
    model_type: str = Field(..., description="模型类型", max_length=50)
    model: str = Field(..., description="具体模型", max_length=50)
    api_key: str = Field(..., description="API密钥", max_length=500)
    proxy_url: Optional[str] = Field(None, description="代理地址(可选)", max_length=200)

class LLMChannelCreate(LLMChannelBase):
    """创建LLM渠道时的Schema"""
    pass

class LLMChannelUpdate(BaseModel):
    """更新LLM渠道时的Schema"""
    channel_name: Optional[str] = Field(None, description="渠道名称", max_length=100)
    model_type: Optional[str] = Field(None, description="模型类型", max_length=50)
    model: Optional[str] = Field(None, description="具体模型", max_length=50)
    api_key: Optional[str] = Field(None, description="API密钥", max_length=500)
    proxy_url: Optional[str] = Field(None, description="代理地址", max_length=200)

class LLMChannel(LLMChannelBase):
    """返回给前端的LLM渠道Schema"""
    id: int
    user_id: int

    class Config:
        from_attributes = True 