from typing import Generic, Optional, TypeVar, Any
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

T = TypeVar('T')

class ResponseCode(str, Enum):
    """
    响应状态码枚举
    """
    SUCCESS = "200"           # 成功
    BAD_REQUEST = "400"       # 请求错误
    UNAUTHORIZED = "401"      # 未授权
    FORBIDDEN = "403"         # 禁止访问
    NOT_FOUND = "404"         # 未找到
    SERVER_ERROR = "500"      # 服务器错误

class ResponseModel(BaseModel, Generic[T]):
    """
    统一响应模型
    """
    code: str = ResponseCode.SUCCESS
    message: str = "Success"
    data: Optional[T] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "code": "200",
                "message": "Success",
                "data": None
            }
        }

def serialize_sqlalchemy(obj: Any) -> Any:
    """
    序列化 SQLAlchemy 模型
    """
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif hasattr(obj, '__dict__'):
        result = {}
        for key, value in obj.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, datetime):
                    result[key] = value.isoformat()
                else:
                    result[key] = value
        return result
    return obj

def response_success(*, data: Any = None, message: str = "Success") -> ResponseModel:
    """
    成功响应
    """
    # 序列化数据
    if data is not None:
        if isinstance(data, (list, tuple)):
            data = [serialize_sqlalchemy(item) for item in data]
        else:
            data = serialize_sqlalchemy(data)
    
    return ResponseModel(
        code=ResponseCode.SUCCESS,
        message=message,
        data=data
    )

def response_error(*, code: str = ResponseCode.BAD_REQUEST, message: str) -> ResponseModel:
    """
    错误响应
    """
    return ResponseModel(
        code=code,
        message=message,
        data=None
    )