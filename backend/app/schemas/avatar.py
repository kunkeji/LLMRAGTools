from typing import Optional
from datetime import datetime
from pydantic import Field, field_validator
from app.schemas.base import BaseSchema
from app.schemas.file import FileUploadResponse, FileUploadConfig

class AvatarConfig(FileUploadConfig):
    """头像上传配置"""
    max_size: int = Field(default=2 * 1024 * 1024, description="最大文件大小(2MB)")
    allowed_types: list[str] = Field(
        default=["image/jpeg", "image/png"],
        description="允许的文件类型"
    )
    image_config: dict = Field(
        default={
            "max_width": 800,
            "max_height": 800,
            "min_width": 100,
            "min_height": 100,
            "quality": 85,
            "formats": ["JPEG", "PNG"]
        },
        description="图片配置"
    )
    storage_config: dict = Field(
        default={
            "path": "avatars",
            "use_timestamp": True,
            "use_uuid": True
        },
        description="存储配置"
    )

    @field_validator('max_size')
    def validate_max_size(cls, v: int) -> int:
        """验证最大文件大小"""
        if v <= 0:
            raise ValueError('最大文件大小必须大于0')
        if v > 5 * 1024 * 1024:  # 5MB
            raise ValueError('头像大小不能超过5MB')
        return v

    @field_validator('allowed_types')
    def validate_allowed_types(cls, v: list[str]) -> list[str]:
        """验证允许的文件类型"""
        valid_types = {"image/jpeg", "image/png"}
        invalid_types = set(v) - valid_types
        if invalid_types:
            raise ValueError(f'不支持的文件类型: {", ".join(invalid_types)}')
        return v

    @field_validator('image_config')
    def validate_image_config(cls, v: dict) -> dict:
        """验证图片配置"""
        if v['max_width'] < v['min_width']:
            raise ValueError('最大宽度不能小于最小宽度')
        if v['max_height'] < v['min_height']:
            raise ValueError('最大高度不能小于最小高度')
        if not (0 <= v['quality'] <= 100):
            raise ValueError('图片质量必须在0-100之间')
        return v

class AvatarUploadResponse(FileUploadResponse):
    """头像上传响应"""
    thumbnail_url: Optional[str] = Field(None, description="缩略图URL")
    width: int = Field(..., description="图片宽度")
    height: int = Field(..., description="图片高度")
    user_id: int = Field(..., description="用户ID")

    @field_validator('width', 'height')
    def validate_dimensions(cls, v: int) -> int:
        """验证图片尺寸"""
        if v <= 0:
            raise ValueError('图片尺寸必须大于0')
        return v

# 默认头像配置
DEFAULT_AVATAR_CONFIG = AvatarConfig() 