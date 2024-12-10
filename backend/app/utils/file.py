import os
import aiofiles
from datetime import datetime
from pathlib import Path
from fastapi import HTTPException, UploadFile
from PIL import Image
import uuid

# 配置上传目录
ROOT_DIR = Path(__file__).parent.parent.parent
STATIC_DIR = ROOT_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
AVATAR_DIR = UPLOAD_DIR / "avatars"
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

# 确保目录存在
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

async def save_avatar(file: UploadFile, user_id: int) -> str:
    """
    保存用户头像
    
    Args:
        file: 上传的文件
        user_id: 用户ID
    
    Returns:
        str: 头像的URL路径
    """
    try:
        # 验证文件大小
        file.file.seek(0, 2)  # 移动到文件末尾
        file_size = file.file.tell()  # 获取文件大小
        file.file.seek(0)  # 重置文件指针
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"文件大小不能超过{MAX_FILE_SIZE/1024/1024}MB"
            )
        
        # 生成文件名
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.jpg', '.jpeg', '.png']:
            raise HTTPException(
                status_code=400,
                detail="不支持的文件类型，仅支持JPG和PNG格式"
            )
        
        # 使用时间戳和随机字符串生成唯一文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_str = uuid.uuid4().hex[:8]
        filename = f"avatar_{user_id}_{timestamp}_{random_str}{file_ext}"
        filepath = AVATAR_DIR / filename
        
        # 保存文件
        async with aiofiles.open(filepath, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # 处理图片
        with Image.open(filepath) as img:
            # 转换为RGB模式（如果是PNG）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 调整图片大小
            max_size = (300, 300)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存处理后的图片
            img.save(filepath, 'JPEG', quality=85)
        
        # 返回相对URL
        return f"/static/uploads/avatars/{filename}"
    
    except Exception as e:
        # 如果保存过程中出现错误，删除已上传的文件
        if 'filepath' in locals() and filepath.exists():
            filepath.unlink()
        raise HTTPException(status_code=500, detail=f"上传文件失败: {str(e)}")

def delete_file(filepath: str) -> bool:
    """
    删除文件
    
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
        full_path = STATIC_DIR / relative_path
        
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    except Exception as e:
        print(f"删除文件失败: {str(e)}")
        return False 