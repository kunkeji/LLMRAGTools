# app/core/security/jwt.py
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from jose import jwt
from app.core.config import settings

def create_access_token(
    subject: Any,
    token_type: str,
    expires_delta: Optional[timedelta] = None,
    extra_data: Optional[Dict[str, Any]] = None,
) -> str:
    """
    创建访问令牌
    Args:
        subject: 令牌主体（用户ID或管理员ID）
        token_type: 令牌类型（user 或 admin）
        expires_delta: 过期时间
        extra_data: 额外数据
    """
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": token_type,
    }
    
    if extra_data:
        to_encode.update(extra_data)
    
    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    验证令牌
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_token
    except jwt.JWTError:
        return None