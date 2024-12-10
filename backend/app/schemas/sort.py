from typing import Optional, List
from enum import Enum
from pydantic import Field, field_validator
from app.schemas.base import BaseSchema

class SortOrder(str, Enum):
    """排序方向"""
    ASC = "asc"
    DESC = "desc"

class SortField(str, Enum):
    """排序字段"""
    # 通用字段
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    
    # 用户相关字段
    USERNAME = "username"
    EMAIL = "email"
    LAST_LOGIN = "last_login"
    STATUS = "status"
    
    # 管理员相关字段
    ROLE = "role"
    FULL_NAME = "full_name"
    
    # 日志相关字段
    LEVEL = "level"
    MODULE = "module"
    TIMESTAMP = "timestamp"

class SortParams(BaseSchema):
    """排序参数"""
    field: SortField = Field(..., description="排序字段")
    order: SortOrder = Field(default=SortOrder.DESC, description="排序方向")

class MultiSortParams(BaseSchema):
    """多字段排序参数"""
    sorts: List[SortParams] = Field(
        default_factory=list,
        max_items=3,
        description="排序参数列表（最���支持3个字段排序）"
    )

    @field_validator('sorts')
    def validate_sorts(cls, v: List[SortParams]) -> List[SortParams]:
        """验证排序参数"""
        if not v:
            return v
        # 检查是否有重复的排序字段
        fields = [sort.field for sort in v]
        if len(fields) != len(set(fields)):
            raise ValueError('排序字段不能重复')
        return v

    def to_sql_order_by(self) -> str:
        """转换为SQL ORDER BY子句"""
        if not self.sorts:
            return "created_at DESC"  # 默认按创建时间倒序
        
        order_by_parts = []
        for sort in self.sorts:
            order_by_parts.append(
                f"{sort.field.value} {sort.order.value.upper()}"
            )
        return ", ".join(order_by_parts) 