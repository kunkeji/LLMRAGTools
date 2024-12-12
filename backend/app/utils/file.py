import os
import aiofiles
from datetime import datetime
from pathlib import Path
from fastapi import HTTPException, UploadFile
from PIL import Image
import uuid
from app.schemas.avatar import DEFAULT_AVATAR_CONFIG, AvatarUploadResponse

# 配置上传目录
ROOT_DIR = Path(__file__).parent.parent.parent
STATIC_DIR = ROOT_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
AVATAR_DIR = UPLOAD_DIR / "avatars"
THUMBNAIL_DIR = AVATAR_DIR / "thumbnails"

# 确保目录存在
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
AVATAR_DIR.mkdir(parents=True, exist_ok=True)
THUMBNAIL_DIR.mkdir(parents=True, exist_ok=True)

async def save_avatar(file: UploadFile, user_id: int) -> AvatarUploadResponse:
    """
    保存用户头像
    
    Args:
        file: 上传的文件
        user_id: 用户ID
    
    Returns:
        AvatarUploadResponse: 头像上传响应
    """
    try:
        # 验证文件大小
        file.file.seek(0, 2)  # 移动到文件末尾
        file_size = file.file.tell()  # 获取文件大小
        file.file.seek(0)  # 重置文件指针
        
        if file_size > DEFAULT_AVATAR_CONFIG.max_size:
            raise HTTPException(
                status_code=400,
                detail=f"文件大小不能超过{DEFAULT_AVATAR_CONFIG.max_size/1024/1024}MB"
            )
        
        # 验证文件类型
        if file.content_type not in DEFAULT_AVATAR_CONFIG.allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型，仅支持: {', '.join(DEFAULT_AVATAR_CONFIG.allowed_types)}"
            )
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_str = uuid.uuid4().hex[:8]
        file_ext = os.path.splitext(file.filename)[1].lower()
        filename = f"avatar_{user_id}_{timestamp}_{random_str}{file_ext}"
        filepath = AVATAR_DIR / filename
        
        # 保存原始文件
        async with aiofiles.open(filepath, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # 处理图片
        with Image.open(filepath) as img:
            # 获取原始尺寸
            original_width, original_height = img.size
            
            # 验证最小尺寸
            if original_width < DEFAULT_AVATAR_CONFIG.image_config['min_width'] or \
               original_height < DEFAULT_AVATAR_CONFIG.image_config['min_height']:
                raise HTTPException(
                    status_code=400,
                    detail=f"图片尺寸太小，最小要求 {DEFAULT_AVATAR_CONFIG.image_config['min_width']}x{DEFAULT_AVATAR_CONFIG.image_config['min_height']}"
                )
            
            # 转换为RGB模式（如果是PNG）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 调整主图大小
            max_size = (
                DEFAULT_AVATAR_CONFIG.image_config['max_width'],
                DEFAULT_AVATAR_CONFIG.image_config['max_height']
            )
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存主图
            img.save(
                filepath,
                'JPEG',
                quality=DEFAULT_AVATAR_CONFIG.image_config['quality']
            )
            
            # 创建缩略图
            thumbnail_size = (100, 100)
            img.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
            thumbnail_filename = f"thumb_{filename}"
            thumbnail_path = THUMBNAIL_DIR / thumbnail_filename
            img.save(
                thumbnail_path,
                'JPEG',
                quality=DEFAULT_AVATAR_CONFIG.image_config['quality']
            )
            
            # 获取处理后的尺寸
            width, height = img.size
        
        # 构建响应
        return AvatarUploadResponse(
            url=f"/static/uploads/avatars/{filename}",
            thumbnail_url=f"/static/uploads/avatars/thumbnails/{thumbnail_filename}",
            filename=filename,
            original_filename=file.filename,
            size=file_size,
            mime_type=file.content_type,
            file_type="image",
            width=width,
            height=height,
            user_id=user_id,
            created_at=datetime.now()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        # 如果保存过程中出现错误，删除已上传的文件
        if 'filepath' in locals():
            if filepath.exists():
                filepath.unlink()
            if 'thumbnail_path' in locals() and thumbnail_path.exists():
                thumbnail_path.unlink()
        raise HTTPException(status_code=500, detail=f"上传文件失败: {str(e)}")

def delete_avatar(filepath: str) -> bool:
    """
    删除头像文件
    
    Args:
        filepath: 文件路径
    
    Returns:
        bool: 是否删除成功
    """
    try:
        # 将URL路径转换为实际文件路径
        relative_path = filepath.lstrip('/')
        if relative_path.startswith('static/'):
            relative_path = relative_path[7:]  # 移除 'static/' 前缀
        
        # 删除主图
        main_path = STATIC_DIR / relative_path
        success = False
        if main_path.exists():
            main_path.unlink()
            success = True
        
        # 尝试删除缩略图
        if 'avatars/' in relative_path:
            thumbnail_path = STATIC_DIR / relative_path.replace('avatars/', 'avatars/thumbnails/thumb_')
            if thumbnail_path.exists():
                thumbnail_path.unlink()
        
        return success
    except Exception as e:
        print(f"删除文件失败: {str(e)}")
        return False 