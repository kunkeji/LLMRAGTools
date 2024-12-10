from typing import Generic, TypeVar, List
from pydantic import Field
from app.schemas.base import BaseSchema

T = TypeVar('T')

class PageParams(BaseSchema):
    """分页参数"""
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=10, ge=1, le=100, description="每页数量")
    
class PageResponse(BaseSchema, Generic[T]):
    """分页响应"""
    total: int = Field(..., description="总数")
    items: List[T] = Field(..., description="数据列表")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")
    has_next: bool = Field(..., description="是否有下一页")
    has_prev: bool = Field(..., description="是否有上一页")

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        page_size: int
    ) -> "PageResponse[T]":
        """
        创建分页响应
        
        Args:
            items: 数据列表
            total: 总数
            page: 当前页码
            page_size: 每页数量
        """
        total_pages = (total + page_size - 1) // page_size
        return cls(
            total=total,
            items=items,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        ) 