# app/core/security/jwt.py
from datetime import datetime, timedelta
from typing import Any, Union, Dict
from jose import jwt
from app.core.config import settings

def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None,
    token_type: str = "user",
    extra_data: Dict[str, Any] = None,
) -> str:
    """
    创建访问令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": token_type,
    }
    
    if extra_data:
        to_encode.update(extra_data)
    
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_token(token: str) -> Dict[str, Any]:
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