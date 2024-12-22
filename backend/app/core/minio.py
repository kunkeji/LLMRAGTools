from minio import Minio
from app.core.config import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE,
)

# 确保必要的bucket存在
def ensure_buckets():
    buckets = [
        "documents",  # 文档存储
        "avatars",   # 用户头像
        "temp",      # 临时文件
    ]
    
    for bucket in buckets:
        if not minio_client.bucket_exists(bucket):
            minio_client.make_bucket(bucket)
            # 设置公共读取权限
            if bucket in ["avatars"]:
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{bucket}/*"]
                        }
                    ]
                }
                minio_client.set_bucket_policy(bucket, policy)

# 文件操作帮助函数
async def upload_file(bucket_name: str, object_name: str, file_path: str, content_type: str = None):
    """上传文件到MinIO"""
    try:
        minio_client.fput_object(
            bucket_name, object_name, file_path,
            content_type=content_type
        )
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

async def download_file(bucket_name: str, object_name: str, file_path: str):
    """从MinIO下载文件"""
    try:
        minio_client.fget_object(bucket_name, object_name, file_path)
        return True
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

async def delete_file(bucket_name: str, object_name: str):
    """删除MinIO中的文件"""
    try:
        minio_client.remove_object(bucket_name, object_name)
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

async def get_file_url(bucket_name: str, object_name: str, expires=3600):
    """获取文件的临时访问URL"""
    try:
        return minio_client.presigned_get_object(
            bucket_name, object_name, expires=expires
        )
    except Exception as e:
        print(f"Error getting file URL: {e}")
        return None 