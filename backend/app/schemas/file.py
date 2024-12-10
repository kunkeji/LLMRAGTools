from typing import Optional, List
from enum import Enum
from datetime import datetime
from pydantic import Field, field_validator
from app.schemas.base import BaseSchema

class FileType(str, Enum):
    """文件类型"""
    IMAGE = "image"
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    OTHER = "other"

class FileUploadResponse(BaseSchema):
    """文件上传响应"""
    url: str = Field(..., description="文件URL")
    filename: str = Field(..., description="文件名")
    original_filename: str = Field(..., description="原始文件名")
    size: int = Field(..., description="文件大小(字节)")
    mime_type: str = Field(..., description="文件MIME类型")
    file_type: FileType = Field(..., description="文件类型")
    width: Optional[int] = Field(None, description="图片宽度(仅图片)")
    height: Optional[int] = Field(None, description="图片高度(仅图片)")
    duration: Optional[float] = Field(None, description="时长(仅视频/音频)")
    created_at: datetime = Field(..., description="上传时间")

class FileInfo(BaseSchema):
    """文件信息"""
    id: int = Field(..., description="文件ID")
    url: str = Field(..., description="文件URL")
    filename: str = Field(..., description="文件名")
    original_filename: str = Field(..., description="原始文件名")
    size: int = Field(..., description="文件大小(字节)")
    mime_type: str = Field(..., description="文件MIME类型")
    file_type: FileType = Field(..., description="文件类型")
    width: Optional[int] = Field(None, description="图片宽度")
    height: Optional[int] = Field(None, description="图片高度")
    duration: Optional[float] = Field(None, description="时长")
    user_id: int = Field(..., description="上传用户ID")
    is_public: bool = Field(..., description="是否公开")
    created_at: datetime = Field(..., description="上传时间")
    updated_at: datetime = Field(..., description="更新时间")

class FileUploadConfig(BaseSchema):
    """文件上传配置"""
    max_size: int = Field(..., description="最大文件大小(字节)")
    allowed_types: List[str] = Field(..., description="允许的文件类型")
    image_config: Optional[dict] = Field(None, description="图片配置")
    video_config: Optional[dict] = Field(None, description="视频配置")
    storage_config: dict = Field(..., description="存储配置")

    @field_validator('max_size')
    def validate_max_size(cls, v: int) -> int:
        """验证最大文件大小"""
        if v <= 0:
            raise ValueError('最大文件大小必须大于0')
        return v

    @field_validator('allowed_types')
    def validate_allowed_types(cls, v: List[str]) -> List[str]:
        """验证允许的文件类型"""
        if not v:
            raise ValueError('允许的文件类型不能为空')
        return v

class FileDeleteResponse(BaseSchema):
    """文件删除响应"""
    success: bool = Field(..., description="是否成功")
    filename: str = Field(..., description="文件名")
    message: Optional[str] = Field(None, description="错误信息") 