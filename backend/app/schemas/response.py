from typing import Generic, Optional, TypeVar, Any, Dict
from pydantic import BaseModel, Field
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
    code: str = Field(default=ResponseCode.SUCCESS, description="响应状态码")
    message: str = Field(default="Success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

def serialize_datetime(obj: Any) -> Any:
    """
    序列化日期时间
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def serialize_model(obj: Any) -> Any:
    """
    序列化模型对象
    """
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif hasattr(obj, 'model_dump'):
        return obj.model_dump()
    elif hasattr(obj, '__dict__'):
        return {
            k: serialize_datetime(v)
            for k, v in obj.__dict__.items()
            if not k.startswith('_')
        }
    return obj

def serialize_data(data: Any) -> Any:
    """
    序列化数据
    """
    if data is None:
        return None
    if isinstance(data, (list, tuple)):
        return [serialize_model(item) for item in data]
    return serialize_model(data)

def response_success(*, data: Any = None, message: str = "Success") -> Dict:
    """
    成功响应
    """
    return {
        "code": ResponseCode.SUCCESS,
        "message": message,
        "data": serialize_data(data)
    }

def response_error(*, code: str = ResponseCode.BAD_REQUEST, message: str) -> Dict:
    """
    错误响应
    """
    return {
        "code": code,
        "message": message,
        "data": None
    }