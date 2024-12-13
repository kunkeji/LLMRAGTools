from typing import Optional, List
from datetime import datetime
from pydantic import Field, field_validator
from app.schemas.base import BaseSchema

class DocumentBase(BaseSchema):
    """文档基础Schema"""
    title: str = Field(..., min_length=1, max_length=200, description="文档标题")
    content: Optional[str] = Field(default="", min_length=0, description="文档内容")
    parent_id: Optional[int] = Field(None, description="父文档ID")
    doc_type: str = Field(default="markdown", description="文档类型：markdown, rich_text, knowledge")
    sort_order: Optional[int] = Field(1, description="排序顺序")

    @field_validator('doc_type')
    def validate_type(cls, v: str) -> str:
        """验证文档类型"""
        valid_types = {'markdown', 'rich_text', 'knowledge', 'tutorial', 'document', 'other'}
        if v not in valid_types:
            raise ValueError('无效的文档类型')
        return v

class DocumentCreate(DocumentBase):
    """创建文档"""
    pass

class DocumentUpdate(BaseSchema):
    """更新文档"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="文档标题")
    content: Optional[str] = Field(None, description="文档内容")
    doc_type: Optional[str] = Field(None, description="文档类型：markdown, rich_text, knowledge")
    sort_order: Optional[int] = Field(None, description="排序顺序")

    @field_validator('doc_type')
    def validate_type(cls, v: Optional[str]) -> Optional[str]:
        """验证文档类型"""
        if v is not None:
            valid_types = {'markdown', 'rich_text', 'knowledge', 'tutorial', 'document', 'other'}
            if v not in valid_types:
                raise ValueError('无效的文档类型')
        return v

class DocumentMove(BaseSchema):
    """移动文档"""
    target_parent_id: Optional[int] = Field(None, description="目标父文档ID")
    sort_order: Optional[int] = Field(None, description="新的排序顺序")

class DocumentInDBBase(DocumentBase):
    """数据库中的文档基础信息"""
    id: int = Field(..., description="文档ID")
    path: str = Field(..., description="文档路径")
    level: int = Field(..., description="文档层级")
    creator_id: Optional[int] = Field(None, description="创建者ID")
    editor_id: Optional[int] = Field(None, description="最后编辑者ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True

class Document(DocumentInDBBase):
    """API响应中的文档信息"""
    children: Optional[List['Document']] = Field(None, description="子文档列表")
    creator_name: Optional[str] = Field(None, description="创建者名称")
    editor_name: Optional[str] = Field(None, description="最后编辑者名称")

class DocumentTree(BaseSchema):
    """文档树节点"""
    id: int = Field(..., description="文档ID")
    title: str = Field(..., description="文档标题")
    doc_type: str = Field(..., description="文档类型")
    level: int = Field(..., description="文档层级")
    sort_order: int = Field(..., description="排序顺序")
    has_children: bool = Field(..., description="是否有子文档")
    children: Optional[List['DocumentTree']] = Field(None, description="子文档列表")

    class Config:
        from_attributes = True 