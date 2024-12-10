from typing import Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """
    基础Schema模型
    """
    model_config = ConfigDict(
        from_attributes=True,  # 支持从ORM模型创建
        populate_by_name=True,  # 支持别名
        use_enum_values=True,  # 使用枚举值
        json_encoders={  # 自定义JSON编码器
            datetime: lambda v: v.isoformat() if v else None
        },
        validate_assignment=True,  # 赋值时验证
        extra='forbid',  # 禁止额外字段
        str_strip_whitespace=True,  # 去除字符串首尾空格
        str_min_length=1,  # 字符串最小长度
        arbitrary_types_allowed=True  # 允许任意类型
    )

    def to_dict(self) -> dict[str, Any]:
        """
        转换为字典
        """
        return self.model_dump(
            exclude_unset=True,  # 排除未设置的字段
            exclude_none=True,   # 排除None值
            by_alias=True        # 使用别名
        )
